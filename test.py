from pathlib import Path
from pipeline import AnimeRecommenderPipeline

pipe = AnimeRecommenderPipeline(Path("data/processed_data.csv"))
print(pipe.get_recommendation("I like action anime with a lot of fighting"))