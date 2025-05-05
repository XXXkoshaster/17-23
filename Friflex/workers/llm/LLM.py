from vllm import LLM, SamplingParams
import json
import torch
import pandas as pd
from common.base_worker import BaseWorker
from common.message import JobType, Message

class LLMWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            worker_type=JobType.LLM,
            input_queue="llm_queue",
            output_queue="translator_queue"
        )
        self.setup_llm()

    def setup_llm(self):
        """Initialize the LLM model"""
        self.llm = LLM(
            model="Qwen/Qwen2.5-14B-Instruct",
            dtype="bfloat16",
            max_num_seqs=128,
            gpu_memory_utilization=0.92,
            max_model_len=32000,
            tensor_parallel_size=1,
            block_size=16,
            enforce_eager=False,
            swap_space=16,
            enable_prefix_caching=True
        )

        self.sampling_params = SamplingParams(
            temperature=0.8,
            top_p=0.92,
            max_tokens=30000,
            frequency_penalty=0.65,
            presence_penalty=0.75,
            repetition_penalty=1.2,
            top_k=40
        )

    def process_message(self, message: Message) -> dict:
        """Process the message and generate chess commentary"""
        # Load and format the game data
        game_data = message.data
        df = pd.json_normalize(game_data['game'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.columns = ['Timestamp', 'Score', 'Best Move', 'Current Move', 'Player']
        md_table = df.to_markdown(index=False, tablefmt='fancy_grid')

        # Prepare the prompt
        prompt_template = """
        Ты — профессиональный шахматный комментатор. Проанализируй данные партии в формате Markdown-таблицы, найди ключевой момент партии длительностью примерно 30 секунд каждый и сгенерируй JSON-отчет для субтитров.

        <<ФОРМАТИРОВАНИЕ ОТВЕТА>>
        1. Строгий синтаксис JSON:
           - Кавычки только двойные
           - Без trailing commas
           - Все числовые значения в миллисекундах

        2. Структура:
        {
          "comments": [
            {
              "start": ["стартовая_метка_времени", "start_date_time"],
              "end": ["конечная_метка_времени", "end_date_time"],
              "comment": "Аналитический текст с: 
                - Шахматной нотацией группы ходов
                - Оценкой критических ходов (для ошибок/для лучших)
                - Названием дебюта/эндшпиля
                - Сравнениями с классическими партиями
                - Эмоциональными акцентами"
            }
          ]
        }

        <<ДАННЫЕ ДЛЯ АНАЛИЗА>>
        {input_data}
        """

        # Generate commentary
        prompts = [prompt_template.format(input_data=md_table)]
        outputs = self.llm.generate(prompts, self.sampling_params)
        
        # Process the output
        generated_text = outputs[0].outputs[0].text
        try:
            commentary = json.loads(generated_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw text
            commentary = {"raw_text": generated_text}

        return {
            "game_data": game_data,
            "commentary": commentary
        }

    def stop(self):
        """Clean up resources"""
        if hasattr(self, 'llm'):
            del self.llm
        super().stop()

if __name__ == "__main__":
    worker = LLMWorker()
    try:
        worker.start()
    except KeyboardInterrupt:
        worker.stop()