import chess
import chess.pgn
from engine import ChessEngine
from io import StringIO
import re



import json





class Parser():

    def __init__(self, path: str):
        self.engine = ChessEngine(path)
        self.board = chess.Board()
        self.white_player_name = "Unknown"
        self.black_player_name = "Unknown"
        
        self.nodes = []
        

    def load_from_str(self, pgn: str):
        self.game = chess.pgn.read_game(StringIO(pgn))
        if self.game:

            self.white_player_name = self.game.headers.get("White", "Unknown")
            self.black_player_name = self.game.headers.get("Black", "Unknown")

            self.board = self.game.board()
            self.nodes = self.game.mainline()

        else:
            print("could not initialize game from file")

    

    def get_opening_from_pgn(self):
        
        for letter in "ABCDE":

            print(f"{letter}")
            # Load ECO database (example: JSON format)
            with open(f"ecodb/eco{letter}.json", encoding="utf-8") as f:
                eco_db = json.loads(f.read())

            board = self.game.board()

            for move in self.game.mainline_moves():
                board.push(move)
                fen = board.fen() # Get position only
                # print(fen)
                # Check against ECO database
                # print(eco_db)
                entry = eco_db.get(fen,0)
                if entry != 0:                
                    print(entry)
                    return entry["eco"], entry["name"]
        
        return None, None

    def analize_current_board(self):
        analysis = self.engine.analyze(self.board)
        return analysis

    def quit(self):
        self.engine.quit()

    def generate_json(self):
        
        fisrt_move_time_offset = 2
        P = 2.5
        D = 2.5

        opening_code, opening_name = self.get_opening_from_pgn()

        game_data = []  

        fisrt_timestamp = None
        last_timestamp = 0
        next_timestamp = 0
        
        time_sum = 0

        for i in range(0, len(list(self.nodes))):

            node = list(self.nodes)[i]

            self.board.push(node.move)

            analisis = parser.analize_current_board()

            player = self.white_player_name 
            if i%2==1:
                player = self.black_player_name 


            # расчет кол-ва фигур на доске, задел на будущее
            material = sum(
                len(self.board.pieces(piece, chess.WHITE)) * value
                for piece, value in [(chess.PAWN, 1), (chess.KNIGHT, 3), (chess.BISHOP, 3),
                                    (chess.ROOK, 5), (chess.QUEEN, 9)]
            ) + sum(
                len(self.board.pieces(piece, chess.BLACK)) * value
                for piece, value in [(chess.PAWN, 1), (chess.KNIGHT, 3), (chess.BISHOP, 3),
                                    (chess.ROOK, 5), (chess.QUEEN, 9)]
            )



            board = node.parent.board()
            san_move = board.san(node.move)

            curr_timestamp = int(re.search(r'\[%ts\s+(\d+)\]', node.comment).group(1))

            if fisrt_timestamp == None:
                fisrt_timestamp = curr_timestamp
                curr_timestamp = 0
            else:
                curr_timestamp = (curr_timestamp - fisrt_timestamp)/1000
            curr_timestamp += fisrt_move_time_offset
            

            
            if i < len(list(self.nodes))-1:
                next_timestamp = (int(re.search(r'\[%ts\s+(\d+)\]', list(self.nodes)[i+1].comment).group(1)) - fisrt_timestamp)/1000 
            next_timestamp += fisrt_move_time_offset


            
            if i == 0:
                timestamp_start = 0
                timestamp_end = curr_timestamp + min((next_timestamp - curr_timestamp)/2, P)
            elif i == len(list(self.nodes))-1:
                timestamp_start = curr_timestamp - min((curr_timestamp - last_timestamp)/2, D)
                timestamp_end = curr_timestamp + P
            else:
                timestamp_start = curr_timestamp - min((curr_timestamp - last_timestamp)/2, D)
                timestamp_end = curr_timestamp + min((next_timestamp - curr_timestamp)/2, P)
                

            print(f"{last_timestamp:2.3f}, {curr_timestamp:2.3f}, {next_timestamp:2.3f}")

            last_timestamp = curr_timestamp


            time_period = timestamp_end - timestamp_start


            timestamp_start = time_sum
            timestamp_end =time_sum + time_period

            best_move="none"
            if analisis["pv"]: best_move = board.san(analisis["pv"][0])
            
            move_data = {
                "time": round(timestamp_end,2), 
                "score": analisis["score"],
                "best": best_move,
                "curr": san_move,
                "who": player
            }
            
            time_sum += time_period
            
            game_data.append(move_data)



        data = {
            "0" : self.white_player_name,
            "1" : self.black_player_name,
            "opening_code": opening_code,
            "opening_name" : opening_name,
            "game" : game_data
        }
        
        print(time_sum)

        return data
    
    


if __name__ == "__main__":
    
    # загрузка движка stockfish
    parser = Parser("stockfish/stockfish-windows-x86-64-avx2.exe")

    # при развертывании необходимо использовать другой бнарный файл
    # parser = AnalAnalizer("stockfish_linux/stockfish-ubuntu-x86-64-avx2")


    # загрузка из строки pgn файла
    # на данный момент строка из файла
    parser.load_from_str(open("./3067/pgn.pgn", encoding="utf-8").read())
    
    data = parser.generate_json()

    # отправка данных дальше по пайплайну
    # на данный момент сохранение в файл
    open("parsed_pgn_data.json","w", encoding="utf-8").write(json.dumps(data, indent=4))
    
    # обязательно закрываем парсер
    parser.quit()