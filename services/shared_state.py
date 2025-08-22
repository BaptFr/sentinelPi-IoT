
class VerificationController:
    def __init__(self):
        self._verification_active = True
        self._enrollment_requested = False
    
    def is_verification_active(self):
        return self._verification_active and not self._enrollment_requested
    
    def request_enrollment(self):
        self._enrollment_requested = True
    
    def enrollment_completed(self):
        self._enrollment_requested = False
        self._verification_active = True

verification_controller = VerificationController()