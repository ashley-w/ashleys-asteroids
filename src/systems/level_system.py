import random

class LevelSystem:
    def __init__(self):
        self.current_level = 1
        self.score_for_next_level = 1000  # Score needed to advance
        self.level_multiplier = 1.5  # Each level requires 50% more score
        
        # 50+ existential level transition messages
        self.existential_messages = [
            "Level 2: You persist. How... quaint.",
            "Level 3: The triangles multiply, much like your regrets.", 
            "Level 4: Still here? The void acknowledges your stubbornness.",
            "Level 5: You're dancing with geometric chaos now.",
            "Level 6: Each shot fired echoes in the endless dark.",
            "Level 7: The asteroids whisper secrets of futility.",
            "Level 8: Your triangle spins, but does it have meaning?",
            "Level 9: Nine levels deep into digital purgatory.",
            "Level 10: Double digits! The universe remains unimpressed.",
            "Level 11: Eleven. A number as arbitrary as your existence here.",
            "Level 12: You've transcended... well, nothing really.",
            "Level 13: Unlucky? Or just another illusion of significance?",
            "Level 14: Fourteen fragments of time wasted beautifully.",
            "Level 15: Fifteen. The asteroids begin to respect your tenacity.",
            "Level 16: Sweet sixteen, but the void doesn't care about birthdays.",
            "Level 17: Seventeen levels of controlled chaos mastered.",
            "Level 18: You're becoming one with the geometric madness.",
            "Level 19: Nineteen reasons why you should have stopped by now.",
            "Level 20: Twenty! A milestone in this triangle-shaped nightmare.",
            "Level 21: Twenty-one. Legal drinking age in space, apparently.",
            "Level 22: The double twos mock you with their symmetry.",
            "Level 23: Twenty-three enigmas wrapped in neon light.",
            "Level 24: Two dozen levels of beautiful digital suffering.",
            "Level 25: Quarter century mark in triangle time.",
            "Level 26: Twenty-six letters in the alphabet of your doom.",
            "Level 27: The cube of three. Mathematics judges you.",
            "Level 28: Twenty-eight days later... still shooting.",
            "Level 29: Twenty-nine steps closer to triangle enlightenment.",
            "Level 30: Thirty! The asteroids file a restraining order.",
            "Level 31: Thirty-one flavors of existential dread.",
            "Level 32: Two to the fifth power. Even math is getting weird.",
            "Level 33: Thirty-three. The cosmic joke deepens.",
            "Level 34: Rule 34: If it exists, there's a level for it.",
            "Level 35: Thirty-five mm of pure, concentrated triangle fury.",
            "Level 36: Six squared. Perfect geometric harmony achieved.",
            "Level 37: Prime number thirty-seven judges your life choices.",
            "Level 38: Thirty-eight special moments of neon-lit violence.",
            "Level 39: Thirty-nine steps to... wait, wrong reference.",
            "Level 40: Forty! The asteroids consider early retirement.",
            "Level 41: Forty-one shades of space madness.",
            "Level 42: The answer to life, universe, and triangle shooting.",
            "Level 43: Forty-three reasons to question reality itself.",
            "Level 44: Double fours. The symmetry is getting suspicious.",
            "Level 45: Halfway to ninety. Math remains your enemy.",
            "Level 46: Forty-six chromosomes of pure gaming dedication.",
            "Level 47: Prime forty-seven whispers ancient gaming secrets.",
            "Level 48: Forty-eight hours of triangle mastery condensed.",
            "Level 49: Forty-nine. One short of something significant.",
            "Level 50: Fifty! Half a century of digital triangle warfare.",
            "Level 51: Fifty-one. You've officially gone too far.",
            "Level 52: Fifty-two weeks in a year of triangle madness.",
            "Level 53: The asteroids have unionized against you.",
            "Level 54: Fifty-four. The number loses all meaning now.",
            "Level 55: Double nickels! Your dedication is both admirable and concerning."
        ]
    
    def get_score_for_level(self, level):
        """Calculate score needed to reach a specific level"""
        if level <= 1:
            return 0
        
        total_score = 0
        current_requirement = 1000
        for i in range(2, level + 1):
            total_score += current_requirement
            current_requirement = int(current_requirement * self.level_multiplier)
        
        return total_score
    
    def check_level_up(self, current_score):
        """Check if player should level up based on current score"""
        next_level_score = self.get_score_for_level(self.current_level + 1)
        if current_score >= next_level_score:
            self.current_level += 1
            return True
        return False
    
    def get_level_message(self):
        """Get existential message for current level"""
        if self.current_level <= len(self.existential_messages):
            return self.existential_messages[self.current_level - 2]  # -2 because level 1 has no message
        else:
            # Generate messages for very high levels
            return f"Level {self.current_level}: You've transcended even our prepared existential dread."
    
    def get_difficulty_multiplier(self):
        """Get difficulty multiplier based on current level"""
        return 1.0 + (self.current_level - 1) * 0.15  # 15% increase per level
    
    def get_asteroid_spawn_rate(self):
        """Get asteroid spawn rate based on level"""
        base_rate = 2.0
        return max(0.5, base_rate - (self.current_level - 1) * 0.1)  # Faster spawning, minimum 0.5 seconds
    
    def get_asteroid_speed_multiplier(self):
        """Get speed multiplier for asteroids based on level"""
        return 1.0 + (self.current_level - 1) * 0.1  # 10% speed increase per level