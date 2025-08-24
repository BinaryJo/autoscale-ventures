from dataclasses import dataclass
from typing import List

@dataclass
class TopicBrief:
    niche: str
    keyword: str
    longtails: list
    score: float

def propose_topics(limit=3) -> List[TopicBrief]:
    c = [
        TopicBrief("utilities", "slugify tool",
                   ["url slug generator","text to slug converter"], 0.72),
        TopicBrief("planning", "time-block planner",
                   ["2-hour blocks","timezone planner"], 0.70),
        TopicBrief("finance", "dividend calendar generator",
                   ["monthly dividend schedule","portfolio payouts"], 0.68),
        TopicBrief("dev", "csv to json converter",
                   ["online csv converter","json formatter"], 0.66),
        TopicBrief("planning", "recurring schedule generator",
                   ["monthly schedule dates","quarterly dates"], 0.64),
    ]
    c.sort(key=lambda x: x.score, reverse=True)
    return c[:limit]
