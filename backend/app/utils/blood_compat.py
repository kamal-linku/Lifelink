"""
Medical Blood Component Compatibility Matrix.
Note: LifeLink uses this for triage matching ranking, but final suitability
remains with qualified blood bank and medical officers.
"""

# Red blood cell compatibility: Recipient -> acceptable Donors
RBC_COMPATIBILITY = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}

# Plasma compatibility (inversed from RBC): Recipient -> acceptable Donors
PLASMA_COMPATIBILITY = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

def is_blood_compatible(donor_group: str, recipient_group: str, component: str = "Packed RBC") -> bool:
    donor = donor_group.strip().upper()
    recipient = recipient_group.strip().upper()

    if component in ["Plasma"]:
        acceptable = PLASMA_COMPATIBILITY.get(recipient, [recipient])
        return donor in acceptable
    else:
        # Packed RBC, Whole Blood, Platelets default
        acceptable = RBC_COMPATIBILITY.get(recipient, [recipient])
        return donor in acceptable

def get_compatible_donor_groups(recipient_group: str, component: str = "Packed RBC") -> list:
    recipient = recipient_group.strip().upper()
    if component == "Plasma":
        return PLASMA_COMPATIBILITY.get(recipient, [recipient])
    return RBC_COMPATIBILITY.get(recipient, [recipient])
