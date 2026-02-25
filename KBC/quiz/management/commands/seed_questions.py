# quiz/management/commands/seed_questions.py

from django.core.management.base import BaseCommand
from quiz.models import Question


QUESTIONS = [

    # ─── LEVEL 1 (Easy) ───────────────────────────────────────
    {
        'text':           'Which planet is known as the Red Planet?',
        'option_a':       'Earth',
        'option_b':       'Mars',
        'option_c':       'Jupiter',
        'option_d':       'Saturn',
        'correct_option': 'B',
        'difficulty':     'easy',
        'level':          1,
    },
    {
        'text':           'How many days are there in a leap year?',
        'option_a':       '365',
        'option_b':       '364',
        'option_c':       '366',
        'option_d':       '367',
        'correct_option': 'C',
        'difficulty':     'easy',
        'level':          1,
    },

    # ─── LEVEL 2 (Easy) ───────────────────────────────────────
    {
        'text':           'What is the capital of France?',
        'option_a':       'Berlin',
        'option_b':       'Madrid',
        'option_c':       'Rome',
        'option_d':       'Paris',
        'correct_option': 'D',
        'difficulty':     'easy',
        'level':          2,
    },
    {
        'text':           'Which gas do plants absorb from the atmosphere?',
        'option_a':       'Oxygen',
        'option_b':       'Nitrogen',
        'option_c':       'Carbon Dioxide',
        'option_d':       'Hydrogen',
        'correct_option': 'C',
        'difficulty':     'easy',
        'level':          2,
    },

    # ─── LEVEL 3 (Easy) ───────────────────────────────────────
    {
        'text':           'What is the chemical symbol for water?',
        'option_a':       'WA',
        'option_b':       'H2O',
        'option_c':       'HO2',
        'option_d':       'OHH',
        'correct_option': 'B',
        'difficulty':     'easy',
        'level':          3,
    },
    {
        'text':           'How many sides does a hexagon have?',
        'option_a':       '5',
        'option_b':       '7',
        'option_c':       '6',
        'option_d':       '8',
        'correct_option': 'C',
        'difficulty':     'easy',
        'level':          3,
    },

    # ─── LEVEL 4 (Easy) ───────────────────────────────────────
    {
        'text':           'Who wrote the play Romeo and Juliet?',
        'option_a':       'Charles Dickens',
        'option_b':       'Leo Tolstoy',
        'option_c':       'William Shakespeare',
        'option_d':       'Mark Twain',
        'correct_option': 'C',
        'difficulty':     'easy',
        'level':          4,
    },
    {
        'text':           'What is the largest ocean on Earth?',
        'option_a':       'Atlantic Ocean',
        'option_b':       'Indian Ocean',
        'option_c':       'Arctic Ocean',
        'option_d':       'Pacific Ocean',
        'correct_option': 'D',
        'difficulty':     'easy',
        'level':          4,
    },

    # ─── LEVEL 5 (Easy — Safe Haven) ─────────────────────────
    {
        'text':           'What is the powerhouse of the cell?',
        'option_a':       'Nucleus',
        'option_b':       'Mitochondria',
        'option_c':       'Ribosome',
        'option_d':       'Golgi Apparatus',
        'correct_option': 'B',
        'difficulty':     'easy',
        'level':          5,
    },
    {
        'text':           'Which country is home to the kangaroo?',
        'option_a':       'Brazil',
        'option_b':       'South Africa',
        'option_c':       'Australia',
        'option_d':       'New Zealand',
        'correct_option': 'C',
        'difficulty':     'easy',
        'level':          5,
    },

    # ─── LEVEL 6 (Medium) ─────────────────────────────────────
    {
        'text':           'What is the speed of light (approx.) in a vacuum?',
        'option_a':       '3 × 10⁸ m/s',
        'option_b':       '3 × 10⁶ m/s',
        'option_c':       '3 × 10¹⁰ m/s',
        'option_d':       '3 × 10⁴ m/s',
        'correct_option': 'A',
        'difficulty':     'medium',
        'level':          6,
    },
    {
        'text':           'Which element has the atomic number 79?',
        'option_a':       'Silver',
        'option_b':       'Platinum',
        'option_c':       'Gold',
        'option_d':       'Copper',
        'correct_option': 'C',
        'difficulty':     'medium',
        'level':          6,
    },

    # ─── LEVEL 7 (Medium) ─────────────────────────────────────
    {
        'text':           'In which year did India gain independence?',
        'option_a':       '1945',
        'option_b':       '1947',
        'option_c':       '1950',
        'option_d':       '1942',
        'correct_option': 'B',
        'difficulty':     'medium',
        'level':          7,
    },
    {
        'text':           'What does CPU stand for?',
        'option_a':       'Central Processing Unit',
        'option_b':       'Core Processing Unit',
        'option_c':       'Central Program Utility',
        'option_d':       'Computer Processing Unit',
        'correct_option': 'A',
        'difficulty':     'medium',
        'level':          7,
    },

    # ─── LEVEL 8 (Medium) ─────────────────────────────────────
    {
        'text':           'Which is the longest river in the world?',
        'option_a':       'Amazon',
        'option_b':       'Yangtze',
        'option_c':       'Mississippi',
        'option_d':       'Nile',
        'correct_option': 'D',
        'difficulty':     'medium',
        'level':          8,
    },
    {
        'text':           'What is the value of Pi (π) up to two decimal places?',
        'option_a':       '3.41',
        'option_b':       '3.14',
        'option_c':       '3.12',
        'option_d':       '3.16',
        'correct_option': 'B',
        'difficulty':     'medium',
        'level':          8,
    },

    # ─── LEVEL 9 (Medium) ─────────────────────────────────────
    {
        'text':           'Who developed the theory of general relativity?',
        'option_a':       'Isaac Newton',
        'option_b':       'Niels Bohr',
        'option_c':       'Albert Einstein',
        'option_d':       'Max Planck',
        'correct_option': 'C',
        'difficulty':     'medium',
        'level':          9,
    },
    {
        'text':           'What is the hardest natural substance on Earth?',
        'option_a':       'Iron',
        'option_b':       'Quartz',
        'option_c':       'Diamond',
        'option_d':       'Graphite',
        'correct_option': 'C',
        'difficulty':     'medium',
        'level':          9,
    },

    # ─── LEVEL 10 (Medium — Safe Haven) ──────────────────────
    {
        'text':           'Which programming language is known as the backbone of the web?',
        'option_a':       'Python',
        'option_b':       'JavaScript',
        'option_c':       'C++',
        'option_d':       'Ruby',
        'correct_option': 'B',
        'difficulty':     'medium',
        'level':          10,
    },
    {
        'text':           'What is the square root of 144?',
        'option_a':       '14',
        'option_b':       '11',
        'option_c':       '13',
        'option_d':       '12',
        'correct_option': 'D',
        'difficulty':     'medium',
        'level':          10,
    },

    # ─── LEVEL 11 (Hard) ──────────────────────────────────────
    {
        'text':           'Which country has the most natural lakes in the world?',
        'option_a':       'Russia',
        'option_b':       'Canada',
        'option_c':       'USA',
        'option_d':       'Finland',
        'correct_option': 'B',
        'difficulty':     'hard',
        'level':          11,
    },
    {
        'text':           'In computing, what does RAM stand for?',
        'option_a':       'Read Access Memory',
        'option_b':       'Random Access Memory',
        'option_c':       'Rapid Access Module',
        'option_d':       'Run Access Memory',
        'correct_option': 'B',
        'difficulty':     'hard',
        'level':          11,
    },

    # ─── LEVEL 12 (Hard) ──────────────────────────────────────
    {
        'text':           'What is the chemical symbol for the element Gold?',
        'option_a':       'Gd',
        'option_b':       'Go',
        'option_c':       'Au',
        'option_d':       'Ag',
        'correct_option': 'C',
        'difficulty':     'hard',
        'level':          12,
    },
    {
        'text':           'Which planet has the most moons in our solar system?',
        'option_a':       'Jupiter',
        'option_b':       'Saturn',
        'option_c':       'Uranus',
        'option_d':       'Neptune',
        'correct_option': 'B',
        'difficulty':     'hard',
        'level':          12,
    },

    # ─── LEVEL 13 (Hard) ──────────────────────────────────────
    {
        'text':           'What is the name of the longest bone in the human body?',
        'option_a':       'Tibia',
        'option_b':       'Humerus',
        'option_c':       'Femur',
        'option_d':       'Fibula',
        'correct_option': 'C',
        'difficulty':     'hard',
        'level':          13,
    },
    {
        'text':           'What does DNA stand for?',
        'option_a':       'Deoxyribonucleic Acid',
        'option_b':       'Dioxynucleic Acid',
        'option_c':       'Diribonucleic Acid',
        'option_d':       'Deoxynitric Acid',
        'correct_option': 'A',
        'difficulty':     'hard',
        'level':          13,
    },

    # ─── LEVEL 14 (Hard) ──────────────────────────────────────
    {
        'text':           'Which mathematician is known as the father of computers?',
        'option_a':       'Alan Turing',
        'option_b':       'Charles Babbage',
        'option_c':       'John von Neumann',
        'option_d':       'Blaise Pascal',
        'correct_option': 'B',
        'difficulty':     'hard',
        'level':          14,
    },
    {
        'text':           'What is the SI unit of electric resistance?',
        'option_a':       'Ampere',
        'option_b':       'Volt',
        'option_c':       'Watt',
        'option_d':       'Ohm',
        'correct_option': 'D',
        'difficulty':     'hard',
        'level':          14,
    },

    # ─── LEVEL 15 (Hard — Final) ──────────────────────────────
    {
        'text':           'What is the only number that cannot be represented in Roman numerals?',
        'option_a':       '0',
        'option_b':       '1000',
        'option_c':       '500',
        'option_d':       '100',
        'correct_option': 'A',
        'difficulty':     'hard',
        'level':          15,
    },
    {
        'text':           'Which ancient wonder of the world was located in Alexandria, Egypt?',
        'option_a':       'Colossus of Rhodes',
        'option_b':       'Hanging Gardens of Babylon',
        'option_c':       'Lighthouse of Alexandria',
        'option_d':       'Temple of Artemis',
        'correct_option': 'C',
        'difficulty':     'hard',
        'level':          15,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample quiz questions'

    def handle(self, *args, **kwargs):
        # Clear existing questions
        Question.objects.all().delete()
        self.stdout.write('Cleared existing questions...')

        # Bulk create all questions
        objs = [Question(**q) for q in QUESTIONS]
        Question.objects.bulk_create(objs)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {len(objs)} questions across 15 levels!'
            )
        )