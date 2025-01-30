# scripts/run_pipeline.py

from app.services.workflow_manager import WorkflowManager

def main():
    workflow = WorkflowManager()
    project_data = workflow.execute_pipeline()

    print("Pipeline completed successfully!")
    print(f"Generated {len(project_data['designs'])} designs")
    print("Market analysis summary:")
    print(json.dumps(project_data['market_analysis'], indent=2))

if __name__ == "__main__":
    main()