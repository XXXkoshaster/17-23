import chess.engine
import os

class ChessEngine:
    def __init__(self, engine_path: str):
        """Initialize the chess engine"""
        if not os.path.exists(engine_path):
            raise FileNotFoundError(f"Engine not found at {engine_path}")
        
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.engine.configure({"Threads": 4, "Hash": 2048})

    def analyze(self, board, time_limit: float = 1.0) -> dict:
        """Analyze the current position"""
        result = self.engine.analyse(
            board,
            chess.engine.Limit(time=time_limit),
            multipv=1
        )
        
        return {
            "score": result["score"].relative.score(mate_score=10000),
            "pv": result.get("pv", []),
            "depth": result.get("depth", 0),
            "nodes": result.get("nodes", 0)
        }

    def quit(self):
        """Quit the engine"""
        if hasattr(self, 'engine'):
            self.engine.quit() 