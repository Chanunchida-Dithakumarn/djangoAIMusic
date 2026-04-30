import uuid  # for generating unique task IDs
import requests
from abc import ABC, abstractmethod
from django.conf import settings


class SongGenerator(ABC):
    @abstractmethod
    def generate(self, song_data: dict) -> dict:
        # get song and send to 'task_id'
        pass

    @abstractmethod
    def check_status(self, task_id: str) -> dict:
        # get task_id and return 'status' and 'song_url'
        pass


class MockSongGenerator(SongGenerator):
    def generate(self, song_data: dict) -> dict:
        fake_task_id = f"mock-task-{uuid.uuid4().hex[:8]}"
        print(f"[Mock] Got order '{song_data.get('title', 'Untitled')}' with task ID: {fake_task_id}")
        
        return {
            "task_id": fake_task_id,
            "status": "Pending"
        }

    def check_status(self, task_id: str) -> dict:
        print(f"[Mock] Song Status: {task_id} completed!")
        
        return {
            "task_id": task_id,
            "status": "Completed",
            "song_url": "https://www.learningcontainer.com/wp-content/uploads/2020/02/Kalimba.mp3"
        }


class SunoSongGenerator(SongGenerator):
    def __init__(self):
        self.api_key = getattr(settings, 'SUNO_API_KEY', '')
        self.base_url = "https://api.sunoapi.org/api/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"}

    def generate(self, song_data: dict) -> dict:
        print("[Suno] - Sending request to Suno API")
        url = f"{self.base_url}/generate"
        
        payload = {
            "prompt": song_data.get('additional', ''),
            "title": song_data.get('title', 'Untitled Song'),
            "tags": f"{song_data.get('genre', 'Pop')}, {song_data.get('mood', '')}",
            "customMode": True,
            "instrumental": False,
            "model": "V4_5ALL",
            "callbackUrl": "https://api.example.com/callback"
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            print("DEBUG STATUS CODE:", response.status_code)
            print("DEBUG RESPONSE TEXT:", response.text)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            
            task_id = None
            if data.get("code") == 200 and "data" in data:
                task_id = data["data"].get("taskId")
            
            print(f"[Suno] - Success! Task ID: {task_id}")
            
            return {
                "task_id": task_id,
                "status": "Pending"
            }

        except requests.exceptions.RequestException as e:
            print(f"[Suno] - Error generating song: {e}")
            return {"task_id": None, "status": "Failed"}

    def check_status(self, task_id: str) -> dict:
        if not task_id:
            return {"task_id": task_id, "status": "Failed", "song_url": ""}

        print(f"[Suno] - Checking status for task_id: {task_id}")
        url = f"{self.base_url}/generate/record-info"
        
        params = {"taskId": task_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            # data = response.json()

            full_data = response.json()
            # print("DEBUG FULL RESPONSE:", full_data)

            data = full_data.get("data") or {}
            
            api_status = data.get("status", "Pending")

            song_url = ""
            response_data = data.get("response") or {}
            suno_data = response_data.get("sunoData") or []

            if suno_data and isinstance(suno_data, list):
                song_url = suno_data[0].get("audioUrl", "")

            if api_status == "SUCCESS":
                status = "Completed"
            elif api_status in ["FAIL", "FAILED", "ERROR"]:
                status = "Failed"
            else:
                status = api_status

            return {
                "task_id": task_id,
                "status": status,
                "song_url": song_url
            }
        except requests.exceptions.RequestException as e:
            print(f"[Suno] - Error checking status: {e}")
            return {"task_id": task_id, "status": "Failed", "song_url": ""}


def get_song_generator() -> SongGenerator:
    # choose Mock or Suno 
    strategy = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()

    if strategy == 'suno':
        print("[System] - Using Suno API Strategy")
        return SunoSongGenerator()
    else:
        print("[System] - Using Mock Strategy")
        return MockSongGenerator()
