import random
from sympy import symbols, solve, diff, Eq
from sympy.parsing.sympy_parser import parse_expr
from typing import Dict, Any

class MathSolver:
    def __init__(self):
        self.problem_types = {
            "house": ["area", "perimeter"],
            "shop": ["area", "perimeter"],
            "factory": ["volume", "area"],
            "park": ["area", "perimeter"]
        }

    def generate_problem(self, building_type: str) -> Dict[str, Any]:
        problem_type = random.choice(self.problem_types[building_type])
        
        if problem_type == "area":
            return self._generate_area_problem(building_type)
        elif problem_type == "perimeter":
            return self._generate_perimeter_problem(building_type)
        elif problem_type == "volume":
            return self._generate_volume_problem(building_type)
        
        raise ValueError(f"Unknown problem type: {problem_type}")

    def _generate_area_problem(self, building_type: str) -> Dict[str, Any]:
        length = random.randint(5, 20)
        width = random.randint(5, 20)
        area = length * width
        
        return {
            "type": "area",
            "question": f"A {building_type} has a length of {length} meters and a width of {width} meters. What is its area in square meters?",
            "answer": str(area)
        }

    def _generate_perimeter_problem(self, building_type: str) -> Dict[str, Any]:
        length = random.randint(5, 20)
        width = random.randint(5, 20)
        perimeter = 2 * (length + width)
        
        return {
            "type": "perimeter",
            "question": f"A {building_type} has a length of {length} meters and a width of {width} meters. What is its perimeter in meters?",
            "answer": str(perimeter)
        }

    def _generate_volume_problem(self, building_type: str) -> Dict[str, Any]:
        length = random.randint(5, 20)
        width = random.randint(5, 20)
        height = random.randint(5, 20)
        volume = length * width * height
        
        return {
            "type": "volume",
            "question": f"A {building_type} has dimensions: length = {length}m, width = {width}m, and height = {height}m. "
                       f"What is its volume in cubic meters?",
            "answer": str(volume)
        }

    def check_answer(self, problem: Dict[str, Any], user_input: str) -> bool:
        try:
            # Parse both the correct answer and user input as expressions
            correct_answer = parse_expr(problem["answer"])
            user_answer = parse_expr(user_input)
            
            # Check if they're equal
            return correct_answer == user_answer
        except:
            # If there's any error in parsing, return False
            return False 