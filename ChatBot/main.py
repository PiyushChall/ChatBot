import json
from difflib import get_close_matches as gcm


def load_mind(file_path: str) -> dict:
  with open(file_path, 'r') as file:
    data: dict = json.load(file)
  return data


def update_mind(file_path: str, data: dict):
  with open(file_path, 'w') as file:
    json.dump(data, file, indent = 2)

def discover_best_match(user_question: str, questions: list[str]) -> str | None:
  matches: list = gcm(user_question, questions, n=1, cutoff = 0.6)
  return matches[0] if matches else None

def get_output_for_userinput(question: str, knowledge_base: dict) -> str | None:
  for q in knowledge_base['questions']:
    if q['question'] == question:
      return  q['answer']

def chat_bot():
  knowledge_base: dict = load_mind('knowledge_base.json')

  while True:
    user_input: str = input("You: ")
    if user_input.lower() == "quit":
      break
    best_match: str | None = discover_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
      answer: str = get_output_for_userinput(best_match, knowledge_base)
      print(f'Bot: {answer}')
    else:
      print("Bot: I don't know the anser can you please teach me !")
      new_answer: str = input('Type the answer or "skip" to Skip: ')
      if new_answer.lower() != "skip":
        knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
        update_mind('knowledge_base.json', knowledge_base)
        print("Bot: Thank You! I learnd a new Response. ")



if __name__ == '__main__':
  chat_bot()