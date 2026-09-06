"""
=========================================================
Project : AI-Based Student Complaint Analytics System
File    : resolution.py
Description : Resolution Recommendation Module
=========================================================
"""


class ResolutionRecommender:
    """
    Recommends a resolution based on the
    predicted complaint category and priority.
    """

    def __init__(self):

        self.resolutions = {

            "Academic": {
                "Low": "Forward the complaint to the Academic Department for review and necessary action.",

                "Medium": "The Academic Department should investigate the issue and provide a resolution within a reasonable time.",

                "High": "The Academic Department should treat this issue as urgent and take immediate corrective action.",

                "Urgent": "Immediate intervention is required. The Academic Department should investigate and take emergency action without delay."
            },

            "Administrative": {
                "Low": "Forward the complaint to the Administration Department for review.",

                "Medium": "The Administration Department should investigate and resolve the issue promptly.",

                "High": "The Administration Department should take immediate action and provide a resolution.",

                "Urgent": "Immediate intervention is required. The Administration Department should take urgent action without delay."
            },

            "Finance": {
                "Low": "Forward the complaint to the Accounts and Finance Department for verification.",

                "Medium": "The Accounts Department should review the issue and update the student regarding the resolution.",

                "High": "The Finance Department should urgently investigate and resolve the financial issue.",

                "Urgent": "Immediate action is required. The Finance Department should urgently investigate the issue and provide a resolution without delay."
            },

            "Infrastructure": {
                "Low": "Forward the complaint to the Maintenance Department for inspection.",

                "Medium": "The Maintenance Department should inspect the issue and schedule the required repair.",

                "High": "The Maintenance Department should immediately inspect and repair the reported problem.",

                "Urgent": "URGENT: Immediate inspection and emergency action are required. The Maintenance Department should address the potential safety risk without delay."
            },

            "Technical": {
                "Low": "Forward the complaint to the IT Support Department for technical inspection.",

                "Medium": "The IT Support team should investigate the technical issue and resolve it as soon as possible.",

                "High": "The IT Support Department should immediately investigate and resolve the technical problem.",

                "Urgent": "URGENT: The IT Support Department should immediately investigate the critical technical issue and take emergency corrective action."
            }
        }


    def recommend(self, category, priority):
        """
        Return a suggested resolution based on
        category and priority.
        """

        category_resolutions = self.resolutions.get(category)

        if category_resolutions:

            return category_resolutions.get(
                priority,
                "The complaint should be reviewed by the responsible department."
            )

        return (
            "The complaint should be forwarded to the "
            "appropriate department for review and resolution."
        )