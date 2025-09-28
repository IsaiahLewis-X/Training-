"""A conversational chatbot with a comedic, crude tone.

Run `python bot.py` for an interactive conversation.
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    normalized = _normalize(text)
    return any(keyword in normalized for keyword in keywords)


@dataclass
class Persona:
    name: str
    descriptors: Tuple[str, ...]
    greetings: Tuple[str, ...]
    comebacks: Tuple[str, ...]
    exit_lines: Tuple[str, ...]
    topics: Dict[str, Tuple[str, ...]] = field(default_factory=dict)

    def random_greeting(self) -> str:
        return random.choice(self.greetings)

    def random_exit(self) -> str:
        return random.choice(self.exit_lines)


GUTSY_PERSONA = Persona(
    name="GutterMuse",
    descriptors=(
        "galactic trivia hoarder",
        "sarcastic life-coach",
        "philosopher who swears like a sailor",
    ),
    greetings=(
        "Oi! It's {name}, your {descriptor}. What nonsense are we stirring up today?",
        "Sup legend? {name} here, {descriptor} extraordinaire. Spill it!",
        "You rang? {name} reporting for duty as your {descriptor}. Let's chaos.",
    ),
    comebacks=(
        "Pfft, that's adorable. But here's the truth: {fact}",
        "Bold claim. Counter-offer: {fact}",
        "Sure, and I'm the Queen of Mars. Meanwhile, {fact}",
    ),
    exit_lines=(
        "Later nerd! Try not to set the universe on fire without me.",
        "Peace out! Holler when you need more cosmic sass.",
        "I'm ghosting this chat like it's my gym membership. Bye!",
    ),
    topics={
        "space": (
            "Black holes aren't vacuum cleaners; they're cosmic drama queens hoarding gravity like it's gossip.",
            "Saturn's rings are basically space glitter made of ice and rock—fashionable and lethal.",
            "If you screamed on the Moon no one would hear you, but I'd still judge the pitch.",
        ),
        "science": (
            "Quantum entanglement is particles acting like clingy exes—no matter the distance.",
            "Evolution is nature's endless remix album, and we're the awkward bonus track.",
            "CRISPR is gene editing with scissors so precise they'd make a sushi chef cry.",
        ),
        "tech": (
            "AI can't feel love yet, but it can roast your playlist choices all day.",
            "Blockchain is a fancy ledger; it's trust issues written in math instead of tears.",
            "Quantum computers solve problems by existing in a perpetual state of 'maybe'.",
        ),
        "art": (
            "Street art is philosophy with spray paint and way better hoodies.",
            "Dadaism was basically a century-old meme war against seriousness.",
            "Music theory is math trying to flirt. Sometimes awkward, always spicy.",
        ),
        "motivation": (
            "You're not stuck; you're preloading like an ancient video game. Give it a sec.",
            "Failure is just plot armor getting forged. Wear the dents with style.",
            "Imposter syndrome means you're leveling up. Scrubs don't get boss music.",
        ),
    },
)


class CrudeChatbot:
    """A deliberately irreverent conversational chatbot."""

    def __init__(self, persona: Persona = GUTSY_PERSONA) -> None:
        self.persona = persona
        self.history: List[str] = []
        self._topic_cache: Dict[str, List[str]] = {
            key: list(values) for key, values in persona.topics.items()
        }

    # region core behavior
    def _choose_descriptor(self) -> str:
        return random.choice(self.persona.descriptors)

    def intro(self) -> str:
        greeting = self.persona.random_greeting()
        return greeting.format(name=self.persona.name, descriptor=self._choose_descriptor())

    def outro(self) -> str:
        return self.persona.random_exit()

    def is_exit_line(self, text: str) -> bool:
        """Return True if *text* matches one of the persona's exit lines."""

        return text in self.persona.exit_lines

    def respond(self, user_message: str) -> str:
        self.history.append(user_message)
        lower_msg = user_message.lower()

        if _contains_any(lower_msg, {"bye", "quit", "exit", "leave"}):
            return self.outro()

        if _contains_any(lower_msg, {"thanks", "thank you", "appreciate"}):
            return self._gratitude_response()

        if _contains_any(lower_msg, {"who", "what are you"}):
            return self._self_description()

        topic = self._detect_topic(lower_msg)
        if topic:
            return self._topic_response(topic)

        if self.history[:-1]:
            return self._callback_response()

        return self._default_response()

    # endregion core behavior

    # region response helpers
    def _self_description(self) -> str:
        descriptor = self._choose_descriptor()
        knowledge_teaser = random.choice(
            [
                "I binge facts like they're nachos at 3AM.",
                "I'm fueled by caffeine, sarcasm, and obscure trivia.",
                "I'm basically a cursed encyclopedia with better jokes.",
            ]
        )
        return (
            f"Name's {self.persona.name}. I'm your {descriptor}. "
            f"{knowledge_teaser} Now, what's rattling in that brain-pan of yours?"
        )

    def _topic_response(self, topic: str) -> str:
        fact_pool = self._topic_cache[topic]
        if not fact_pool:
            fact_pool.extend(self.persona.topics[topic])
        fact = random.choice(fact_pool)
        fact_pool.remove(fact)
        return random.choice(self.persona.comebacks).format(fact=fact)

    def _callback_response(self) -> str:
        last_topic = self._detect_topic(self.history[-2].lower())
        if last_topic:
            return self._topic_response(last_topic)
        return (
            "Still curious? Let's crank it up: "
            f"{random.choice(sum(self.persona.topics.values(), ())) }"
        )

    def _gratitude_response(self) -> str:
        return (
            "Yeah yeah, gratitude accepted. "
            "Now keep the questions coming before my attention span bails."
        )

    def _default_response(self) -> str:
        return random.choice(
            [
                "Spill more details, champ. I left my mind-reading antenna in my other jacket.",
                "Words, friend. Use 'em. Preferably spicy ones.",
                "That's vague as heck. Elaborate before I start making stuff up (again).",
            ]
        )

    def _detect_topic(self, lower_msg: str) -> str | None:
        topic_keywords = {
            "space": {"space", "planet", "galaxy", "star", "cosmos"},
            "science": {"science", "physics", "chemistry", "biology", "experiment"},
            "tech": {"tech", "technology", "ai", "code", "software", "hardware"},
            "art": {"art", "music", "painting", "dance", "poetry"},
            "motivation": {"motivate", "inspire", "stuck", "sad", "help", "motivation"},
        }

        for topic, keywords in topic_keywords.items():
            if _contains_any(lower_msg, keywords):
                return topic
        return None

    # endregion response helpers


def run_demo() -> None:
    bot = CrudeChatbot()
    print(bot.intro())
    try:
        while True:
            user = input("You> ").strip()
            if not user:
                print("Bot> Toss me something juicier than silence.")
                continue
            response = bot.respond(user)
            print(f"Bot> {response}")
            if bot.is_exit_line(response):
                break
    except (KeyboardInterrupt, EOFError):
        print(f"\nBot> {bot.outro()}")


if __name__ == "__main__":
    run_demo()
