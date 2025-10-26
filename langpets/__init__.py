from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
import time, threading, sys, queue

console = Console()

class Pet:
    def __init__(self, name="Turtly"):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.mood = "neutral"
        self.smacks = 0
        self.good_actions = 0
        self.frame_index = 0

        # Expressions by mood
        self.expressions = {
            "happy": [
r"""
   _____     
 /       \   
|  ^   ^  |  
|    ∇    |  
 \__‾‾‾__/   
   || ||     
  _|| ||_
""",
r"""
   _____     
 /       \   
|  o   ^  |  
|    ∇    |  
 \__‾‾‾__/   
   || ||     
  _|| ||_
"""
            ],
            "neutral": [
r"""
   _____     
 /       \   
|  o   o  |  
|    ∇    |  
 \__‾‾‾__/   
   || ||     
  _|| ||_
"""
            ],
            "sad": [
r"""
   _____     
 /       \   
|  -   -  |  
|    ∇    |  
 \__..__/   
   || ||     
  _|| ||_
""",
r"""
   _____     
 /       \   
|  -   o  |  
|    ∇    |  
 \__..__/   
   || ||     
  _|| ||_
"""
            ]
        }

    def update_mood(self):
        if self.good_actions > self.smacks:
            self.mood = "happy"
        elif self.good_actions < self.smacks:
            self.mood = "sad"
        else:
            self.mood = "neutral"

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.good_actions += 1
        self.update_mood()
        return f"You feed {self.name}. 🍎 Hunger now {self.hunger}/100"

    def play(self):
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy - 5)
        self.good_actions += 1
        self.update_mood()
        return f"You play with {self.name}! 🎾 Happiness now {self.happiness}/100"

    def smack(self):
        self.happiness = max(0, self.happiness - 10)
        self.smacks += 1
        self.update_mood()
        return f"You smack {self.name}... 😢 Happiness now {self.happiness}/100"

    def tick(self):
        # Decay and tiredness over time
        self.hunger = min(100, self.hunger + 0.3)
        self.happiness = max(0, self.happiness - 0.1)
        self.energy = max(0, self.energy - 0.05)

    def get_frame(self):
        frames = self.expressions[self.mood]
        frame = frames[self.frame_index % len(frames)]
        self.frame_index += 1
        return frame

    def mood_color(self):
        return {
            "happy": "green",
            "neutral": "yellow",
            "sad": "red"
        }[self.mood]


def pet_display(pet):
    frame = pet.get_frame()
    pet_info = (
        f"[bold {pet.mood_color()}]🐢 {pet.name}[/bold {pet.mood_color()}] ({pet.mood})\n"
        f"Hunger: {int(pet.hunger)} | Happiness: {int(pet.happiness)} | Energy: {int(pet.energy)}"
    )
    panel = Panel.fit(
        Text(frame, style=pet.mood_color()),
        title=pet_info,
        border_style=pet.mood_color(),
    )
    return panel


def input_thread(q):
    while True:
        q.put(console.input("[cyan]\nWhat do you want to do?[/cyan]\n[1] Feed 🍎  [2] Play 🎾  [3] Smack 👋  [4] Quit ❌\n> "))


def run():
    pet = Pet()
    q = queue.Queue()
    threading.Thread(target=input_thread, args=(q,), daemon=True).start()

    with Live(console=console, refresh_per_second=4) as live:
        while True:
            pet.tick()
            live.update(pet_display(pet))

            if not q.empty():
                choice = q.get().strip()
                if choice == "1":
                    console.print(f"[green]{pet.feed()}[/green]")
                elif choice == "2":
                    console.print(f"[yellow]{pet.play()}[/yellow]")
                elif choice == "3":
                    console.print(f"[red]{pet.smack()}[/red]")
                elif choice == "4":
                    console.print("[magenta]Goodbye![/magenta]")
                    sys.exit(0)
                else:
                    console.print("[red]Invalid choice![/red]")

            time.sleep(0.6)


if __name__ == "__main__":
    run()
