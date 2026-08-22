class NotificationService:
    def send_submission_notification(
        self,
        widget_id: int,
        submission_id: int,
    ) -> None:
        print(
            f"New submission {submission_id} "
            f"received for widget {widget_id}"
        )