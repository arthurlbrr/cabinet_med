class PatientNotFoundError(Exception):
    """Le patient demandé n'existe pas."""
    pass


class ConsultationNotFoundError(Exception):
    """La consultation demandée n'existe pas."""
    pass


class InvalidSecurityNumberError(Exception):
    """Le numéro de sécurité sociale est invalide."""
    pass


class InvalidConsultationStatusError(Exception):
    """Statut de consultation invalide pour l'opération demandée."""
    pass
