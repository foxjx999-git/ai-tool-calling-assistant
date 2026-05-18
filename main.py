from ai_client import ask_ai

def main():
     print("AI Tool Calling 最小版学习助手已启动。输入 exit 退出。")

     while True:
        user_input = input("\n你：").strip()
        if user_input.lower() == "exit" or user_input.lower() == "q":
            print("已退出。")
            break
          
        if not user_input:
            continue

        try:
            answer = ask_ai(user_input)
            print("\nAI: ", answer)

        except Exception as e:
            print(f"\n程序出错：{e}")


if __name__ == "__main__":
    main()



