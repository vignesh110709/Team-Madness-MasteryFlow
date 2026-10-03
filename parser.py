import re
import json

def parse():
    with open("raw_qs.txt", "r", encoding="utf-8") as f:
        q_lines = f.read().split('\n')
        
    with open("raw_ans.txt", "r", encoding="utf-8") as f:
        ans_lines = f.read().split('\n')
        
    # Parse answers
    ans_map = {}
    for line in ans_lines:
        line = line.strip()
        if not line: continue
        parts = line.split(' ', 3)
        if len(parts) >= 3:
            qnum = int(parts[0])
            ans_char = parts[2]
            ans_map[qnum] = ans_char
            
    # Parse questions
    # Format: [ID, Concept, Difficulty(1-4), Type, QuestionText, [Options], CorrectAnswerText, Explanation]
    Q = []
    
    current_subject = "Computer Science"
    current_diff = 1 # 1: Easy, 3: Medium, 4: Difficult
    
    q_pattern = re.compile(r'^Q(\d+)\.\s+(.*)$')
    opt_pattern = re.compile(r'^([A-D])\.\s+(.*)$')
    
    curr_q = None
    
    for line in q_lines:
        line = line.strip()
        if not line: continue
        
        if line in ["Computer Science", "Biology", "Physics", "Chemistry"]:
            current_subject = line
            continue
            
        if line == "● EASY LEVEL":
            current_diff = 1
            continue
        elif line == "● MEDIUM LEVEL":
            current_diff = 3
            continue
        elif line == "● DIFFICULT LEVEL":
            current_diff = 4
            continue
            
        q_match = q_pattern.match(line)
        if q_match:
            if curr_q:
                Q.append(curr_q)
            qnum = int(q_match.group(1))
            qtext = q_match.group(2)
            curr_q = {
                "id": f"{current_subject[:3].upper()}{qnum}",
                "concept": current_subject,
                "diff": current_diff,
                "type": "MCQ",
                "text": qtext,
                "options": [],
                "qnum": qnum
            }
            continue
            
        opt_match = opt_pattern.match(line)
        if opt_match and curr_q:
            curr_q["options"].append(opt_match.group(2))
            continue
            
        # Continuation of previous line if no match
        if curr_q and len(curr_q["options"]) == 0:
            curr_q["text"] += " " + line
            
    if curr_q:
        Q.append(curr_q)
        
    # Formulate final tuples
    final_Q = []
    for q in Q:
        ans_char = ans_map.get(q["qnum"])
        if ans_char == 'A': correct = q["options"][0]
        elif ans_char == 'B': correct = q["options"][1]
        elif ans_char == 'C': correct = q["options"][2]
        else: correct = q["options"][3]
        
        final_Q.append((
            q["id"],
            q["concept"],
            q["diff"],
            q["type"],
            q["text"],
            q["options"],
            correct,
            f"Correct answer is {correct}."
        ))
        
    with open("questions_db.py", "w", encoding="utf-8") as f:
        f.write('PREREQS = {\n    "Computer Science": [],\n    "Biology": [],\n    "Physics": [],\n    "Chemistry": []\n}\n\n')
        f.write("Q = [\n")
        for item in final_Q:
            f.write(f"    {repr(item)},\n")
        f.write("]\n")

if __name__ == "__main__":
    parse()
