import re

def fix():
    # Read the existing questions_db.py
    with open("questions_db.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # We will just rewrite questions_db.py from scratch to guarantee it's perfect
    
    with open("parser.py", "r", encoding="utf-8") as f:
        parser_code = f.read()
        
    # Run the original parser to get the 60 questions back
    import parser
    parser.parse()
    
    # Now questions_db.py has 60 questions. Let's append math correctly.
    math_q = [
        ('MAT61', 'Mathematics', 1, 'MCQ', 'What is 7 x 8?', ['54', '64', '48', '56'], '56', 'Correct answer is 56.'),
        ('MAT62', 'Mathematics', 1, 'MCQ', 'What is the approximate value of pi?', ['2.14', '3.14', '3.41', '4.13'], '3.14', 'Correct answer is 3.14.'),
        ('MAT63', 'Mathematics', 1, 'MCQ', 'What is the sum of the interior angles of a triangle?', ['90°', '180°', '270°', '360°'], '180°', 'Correct answer is 180°.'),
        ('MAT64', 'Mathematics', 1, 'MCQ', 'What is the square root of 144?', ['13', '12', '11', '14'], '12', 'Correct answer is 12.'),
        ('MAT65', 'Mathematics', 1, 'MCQ', 'What is 25% of 200?', ['75', '40', '50', '25'], '50', 'Correct answer is 50.'),
        ('MAT66', 'Mathematics', 3, 'MCQ', 'Solve for x: 3x + 5 = 20', ['x = 5', 'x = 6', 'x = 4', 'x = 15'], 'x = 5', 'Correct answer is x = 5.'),
        ('MAT67', 'Mathematics', 3, 'MCQ', 'What is the area of a circle of radius 7 units? (take pi = 22/7)', ['49 square units', '44 square units', '154 square units', '308 square units'], '154 square units', 'Correct answer is 154 square units.'),
        ('MAT68', 'Mathematics', 3, 'MCQ', 'What is the derivative of x^3 with respect to x?', ['x^4/4', 'x^2', '3x^2', '3x'], '3x^2', 'Correct answer is 3x^2.'),
        ('MAT69', 'Mathematics', 3, 'MCQ', 'What is the sum of the first 10 natural numbers?', ['55', '50', '100', '45'], '55', 'Correct answer is 55.'),
        ('MAT70', 'Mathematics', 3, 'MCQ', 'What are the roots of x^2 - 5x + 6 = 0?', ['2 and 3', '1 and 6', '-2 and -3', '-1 and -6'], '2 and 3', 'Correct answer is 2 and 3.'),
        ('MAT71', 'Mathematics', 4, 'MCQ', 'Evaluate the definite integral of 2x dx from x = 0 to x = 3.', ['3', '6', '9', '18'], '9', 'Correct answer is 9.'),
        ('MAT72', 'Mathematics', 4, 'MCQ', 'Two fair dice are rolled. What is the probability that the sum is 7?', ['7/36', '1/6', '1/12', '1/9'], '1/6', 'Correct answer is 1/6.'),
        ('MAT73', 'Mathematics', 4, 'MCQ', 'In how many distinct ways can the letters of the word LEVEL be arranged?', ['120', '24', '30', '60'], '30', 'Correct answer is 30.'),
        ('MAT74', 'Mathematics', 4, 'MCQ', 'What is the value of log2(64) + log3(9)?', ['12', '10', '8', '6'], '8', 'Correct answer is 8.'),
        ('MAT75', 'Mathematics', 4, 'MCQ', 'What is the determinant of the 2x2 matrix with rows (2, 3) and (1, 4)?', ['5', '11', '8', '3'], '5', 'Correct answer is 5.')
    ]
    
    with open("questions_db.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Safely replace PREREQS
    content = content.replace('"Chemistry": []\n}', '"Chemistry": [],\n    "Mathematics": []\n}')

    # Safely append to Q
    # Find the last bracket of Q
    content = content.strip()
    if content.endswith(']'):
        content = content[:-1] # remove last bracket
        if not content.endswith(','):
            content += ',\n'
        for item in math_q:
            content += f"    {repr(item)},\n"
        content += "]\n"
        
    with open("questions_db.py", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    fix()
