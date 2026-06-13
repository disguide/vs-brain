from src.workflows.information_gathering import InformationGatheringWorkflow

def main():
    workflow = InformationGatheringWorkflow()
    result = workflow.run("What are the best RAG architectures for production LLM systems in 2026?")

    if result.needs_clarification:
        print("\nClarification needed before proceeding.")
        return

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result.final_summary)

if __name__ == "__main__":
    main()
