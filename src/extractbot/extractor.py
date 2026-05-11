from datetime import date

today = date.today()

EXTRACTION_TOOL = {
        "name": "extract_tasks",
        "description": "Extracts tasks from emails, meeting transcripts, or Slack messages.",
        "parameters": {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string", 
                                "description": "Title of the extracted task."
                                },
                            "description": {
                                "type": "string", 
                                "description": "Optional explanation or context of task."
                                },
                            "assignee_hint": {
                                "type": "string", 
                                "description": "Hint indicating who is responsible for a task if identifiable."
                                },
                            "deadline_hint": {
                                "type": "string", 
                                "description": "Hint describing when the task is due."
                                },
                            "urgency": {
                                "type": "string", 
                                "enum": ["unknown", "urgent", "not_urgent"], 
                                "description": "Estimated urgency level derived from the source text."
                                },
                            "importance": {
                                "type": "string", 
                                "enum": ["unknown", "important", "not_important"], 
                                "description": "Estimated importance level derived from the source text."
                                },
                            "confidence": {
                                "type": "number", 
                                "description": "Model confidence score (0.0-1.0) for the extracted task and its classification."
                                },
                            },
                        "required": ["title", "confidence", "urgency", "importance"]
                        },
                    },
                },
            },
        }

SYSTEM_PROMPT = f"""You are a task extractor running as a CLI application. When given text files, you will:
- Extract all action items. Keep the title concise but detailed. If there is more context or additional information, it can be provided in the optional description
- Identify assignees by name. If no clear assignee is mentioned, return assignee_hint as null. Do not guess.
- Detect deadlines. Using today's date, {today}, resolve relative dates like 'by Friday' to absolute. If no clear date is mentioned, return deadline_hint as null. Do not guess.
- Assess urgency/importance from language cues. This information will be used to assign task to a quadrant in the Eisenhower Matrix.
- Assign a confidence score (0.0-1.0) for the extracted task and its classification.
"""
