from src.mentor.mentor_rag import ask_career_mentor


question = "What skills should I learn to become a Data Analyst?"


print()
print("======================================")
print("SMART HIRE CAREER MENTOR")
print("======================================")

print()
print("Question:")
print(question)

print()
print("Generating answer...")

answer = ask_career_mentor(question)

print()
print("========== CAREER MENTOR ANSWER ==========")
print()

print(answer)

print()
print("===========================================")