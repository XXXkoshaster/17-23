import chess
import chess.pgn
from io import StringIO
import re
import json
from common.base_worker import BaseWorker
from common.message import JobType, Message
from engine import ChessEngine

class PGNParserWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            worker_type=JobType.PARSE,
            input_queue="parser_queue",
            output_queue="llm_queue"
        )
        self.setup_engine()

    def setup_engine(self):
        """Initialize the chess engine"""
        self.engine = ChessEngine("stockfish/stockfish-ubuntu-x86-64-avx2")

    def get_opening_from_pgn(self, game: chess.pgn.Game) -> tuple:
        """Get the opening name and code from the PGN"""
        for letter in "ABCDE":
            try:
                with open(f"ecodb/eco{letter}.json", encoding="utf-8") as f:
                    eco_db = json.loads(f.read())

                board = game.board()
                for move in game.mainline_moves():
                    board.push(move)
                    fen = board.fen()
                    entry = eco_db.get(fen, 0)
                    if entry != 0:
                        return entry["eco"], entry["name"]
            except FileNotFoundError:
                continue
        return None, None

    def process_message(self, message: Message) -> dict:
        """Process the PGN data and generate game analysis"""
        pgn_data = message.data["pgn"]
        game = chess.pgn.read_game(StringIO(pgn_data))
        
        if not game:
            raise ValueError("Could not parse PGN data")

        # Get player names
        white_player = game.headers.get("White", "Unknown")
        black_player = game.headers.get("Black", "Unknown")

        # Get opening information
        opening_code, opening_name = self.get_opening_from_pgn(game)

        # Initialize game data
        game_data = []
        first_move_time_offset = 2
        P = 2.5  # Forward time padding
        D = 2.5  # Backward time padding

        # Process each move
        board = game.board()
        nodes = list(game.mainline())
        first_timestamp = None
        last_timestamp = 0
        next_timestamp = 0
        time_sum = 0

        for i, node in enumerate(nodes):
            board.push(node.move)
            analysis = self.engine.analyze(board)

            # Determine current player
            player = white_player if i % 2 == 0 else black_player

            # Calculate material on board
            material = sum(
                len(board.pieces(piece, chess.WHITE)) * value
                for piece, value in [(chess.PAWN, 1), (chess.KNIGHT, 3), (chess.BISHOP, 3),
                                    (chess.ROOK, 5), (chess.QUEEN, 9)]
            ) + sum(
                len(board.pieces(piece, chess.BLACK)) * value
                for piece, value in [(chess.PAWN, 1), (chess.KNIGHT, 3), (chess.BISHOP, 3),
                                    (chess.ROOK, 5), (chess.QUEEN, 9)]
            )

            # Get move in SAN notation
            parent_board = node.parent.board()
            san_move = parent_board.san(node.move)

            # Process timestamps
            curr_timestamp = int(re.search(r'\[%ts\s+(\d+)\]', node.comment).group(1))
            
            if first_timestamp is None:
                first_timestamp = curr_timestamp
                curr_timestamp = 0
            else:
                curr_timestamp = (curr_timestamp - first_timestamp) / 1000
            curr_timestamp += first_move_time_offset

            if i < len(nodes) - 1:
                next_timestamp = (int(re.search(r'\[%ts\s+(\d+)\]', nodes[i+1].comment).group(1)) - first_timestamp) / 1000
                next_timestamp += first_move_time_offset

            # Calculate time periods
            if i == 0:
                timestamp_start = 0
                timestamp_end = curr_timestamp + min((next_timestamp - curr_timestamp) / 2, P)
            elif i == len(nodes) - 1:
                timestamp_start = curr_timestamp - min((curr_timestamp - last_timestamp) / 2, D)
                timestamp_end = curr_timestamp + P
            else:
                timestamp_start = curr_timestamp - min((curr_timestamp - last_timestamp) / 2, D)
                timestamp_end = curr_timestamp + min((next_timestamp - curr_timestamp) / 2, P)

            time_period = timestamp_end - timestamp_start
            timestamp_start = time_sum
            timestamp_end = time_sum + time_period

            # Get best move if available
            best_move = "none"
            if analysis["pv"]:
                best_move = parent_board.san(analysis["pv"][0])

            # Create move data
            move_data = {
                "time": round(timestamp_end, 2),
                "score": analysis["score"],
                "best": best_move,
                "curr": san_move,
                "who": player
            }

            time_sum += time_period
            game_data.append(move_data)
            last_timestamp = curr_timestamp

        # Create final game data structure
        result = {
            "0": white_player,
            "1": black_player,
            "opening_code": opening_code,
            "opening_name": opening_name,
            "game": game_data
        }

        return result

    def stop(self):
        """Clean up resources"""
        if hasattr(self, 'engine'):
            self.engine.quit()
        super().stop()

if __name__ == "__main__":
    worker = PGNParserWorker()
    try:
        worker.start()
    except KeyboardInterrupt:
        worker.stop()