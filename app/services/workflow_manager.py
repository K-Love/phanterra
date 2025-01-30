# app/services/workflow_manager.py

from typing import List, Dict
import json
import os
from datetime import datetime
from functools import wraps

from .niche_analyzer import NicheAnalyzer
from .design_generator import DesignGenerator
from .blockchain_service import BlockchainService
from .kdp_uploader import KDPUploader
from .error_handler import ErrorHandler
from .monitoring import MonitoringService
from .marketing_automation import MarketingAutomation

class WorkflowManager:
    def __init__(self):
        # Core services
        self.niche_analyzer = NicheAnalyzer()
        self.design_generator = DesignGenerator()
        self.blockchain_service = BlockchainService()
        self.kdp_uploader = KDPUploader()

        # Support services
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringService()
        self.marketing = MarketingAutomation()

    def execute_pipeline(self, pages_per_book=50, save_data=True):
        """
        Execute the complete workflow pipeline with monitoring and error handling
        """
        project_data = {
            "timestamp": datetime.now().isoformat(),
            "pages_per_book": pages_per_book,
            "id": f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }

        monitoring_data = self.monitoring.start_monitoring({
            'pipeline_start': project_data["timestamp"],
            'project_id': project_data["id"],
            'pages_per_book': pages_per_book
        })

        try:
            # Execute core pipeline steps
            project_data.update(self._execute_core_steps(pages_per_book))

            # Execute marketing automation
            project_data['marketing'] = self.marketing.create_marketing_campaign(project_data)

            # Record success
            self._record_success(project_data["id"])
            project_data["status"] = "success"

        except Exception as e:
            # Handle failure
            self._record_failure(project_data["id"], e)
            project_data["status"] = "failed"
            project_data["error"] = str(e)
            raise

        finally:
            # Finalize monitoring and save data
            project_data['monitoring_summary'] = self.monitoring.end_monitoring(monitoring_data)

            if save_data:
                self._save_project_data(project_data)

        return project_data

    def _execute_core_steps(self, pages_per_book: int) -> Dict:
        """
        Execute the core pipeline steps
        """
        results = {}

        # 1. Market Research
        print("Analyzing market trends...")
        bestsellers = self.niche_analyzer.get_amazon_bestsellers()
        trends = self.niche_analyzer.analyze_trends(bestsellers)
        niches = self.niche_analyzer.get_top_niches(trends)
        results['market_analysis'] = trends
        results['niches'] = niches

        # 2. Design Generation
        print("Generating designs...")
        designs = self.design_generator.batch_generate(
            niches=niches,
            pages_per_book=pages_per_book
        )
        results['designs'] = designs

        # 3. NFT Minting
        print("Minting NFTs...")
        nft_ids = self.blockchain_service.mint_batch(designs)
        results['nft_ids'] = nft_ids

        # 4. KDP Upload
        print("Uploading to KDP...")
        kdp_results = self.kdp_uploader.upload_batch(designs)
        results['kdp_results'] = kdp_results

        return results

    def _record_success(self, project_id: str):
        """
        Record successful pipeline execution
        """
        self.monitoring.record_metric(
            'pipeline_success_rate',
            1.0,
            {'project_id': project_id}
        )

    def _record_failure(self, project_id: str, error: Exception):
        """
        Record pipeline failure
        """
        self.monitoring.record_metric(
            'pipeline_success_rate',
            0.0,
            {'project_id': project_id}
        )

        self.error_handler.handle_error(
            error,
            {'project_id': project_id}
        )

    def _save_project_data(self, data: Dict):
        """
        Save project data to JSON file
        """
        filename = f"project_data_{data['id']}.json"
        os.makedirs("data", exist_ok=True)

        filepath = os.path.join("data", filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Project data saved to: {filepath}")
        return filepath

    def get_project_status(self, project_id: str) -> Dict:
        """
        Get status of a specific project
        """
        filepath = os.path.join("data", f"project_data_{project_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {"error": "Project not found"}

    def retry_failed_steps(self, project_id: str) -> Dict:
        """
        Retry failed steps in a project
        """
        project_data = self.get_project_status(project_id)
        if project_data.get("status") != "failed":
            return {"error": "Project is not in failed state"}

        # Implementation for retry logic
        return self.execute_pipeline(
            pages_per_book=project_data.get("pages_per_book", 50),
            save_data=True
        )

# Created/Modified files:
# - data/project_data_{project_id}.json