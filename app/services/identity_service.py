from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.contact import Contact, LinkPrecedence


def identify_contact(db: Session, email: str, phone: str):

    with db.begin():   # transaction block to ensure atomicity
        # Check for existing contacts with given email or phone
        existing_contacts = db.query(Contact).filter(
            or_(
                Contact.email == email,
                Contact.phoneNumber == phone
            )
        ).all()

        # If no existing contact → create primary
        if not existing_contacts:
            new_contact = Contact(
                email=email,
                phoneNumber=phone,
                linkPrecedence=LinkPrecedence.primary
            )
            db.add(new_contact)
            db.flush()  # get ID without committing

            return build_response(db, new_contact.id)

        # Collect primary IDs
        primary_ids = set()

        for contact in existing_contacts:
            if contact.linkPrecedence == LinkPrecedence.primary:
                primary_ids.add(contact.id)
            else:
                primary_ids.add(contact.linkedId)

        primaries = db.query(Contact).filter(
            Contact.id.in_(primary_ids)
        ).all()

        # Oldest becomes primary
        primary = sorted(primaries, key=lambda x: x.createdAt)[0]

        # Convert other primaries to secondary
        for p in primaries:
            if p.id != primary.id:
                p.linkPrecedence = LinkPrecedence.secondary
                p.linkedId = primary.id

        # Create secondary if new info
        existing_emails = {c.email for c in existing_contacts if c.email}
        existing_phones = {c.phoneNumber for c in existing_contacts if c.phoneNumber}

        if (email and email not in existing_emails) or (
            phone and phone not in existing_phones
        ):
            new_secondary = Contact(
                email=email,
                phoneNumber=phone,
                linkedId=primary.id,
                linkPrecedence=LinkPrecedence.secondary
            )
            db.add(new_secondary)

    # transaction block ends, changes will be committed

    return build_response(db, primary.id)


# Helper function to build the response based on primary contact ID
def build_response(db: Session, primary_id: int):

    contacts = db.query(Contact).filter(
        (Contact.id == primary_id) |
        (Contact.linkedId == primary_id)
    ).all()

    primary = [c for c in contacts if c.id == primary_id][0]

    secondary_ids = [c.id for c in contacts if c.id != primary_id]

    emails = list(dict.fromkeys([c.email for c in contacts if c.email]))
    phones = list(dict.fromkeys([c.phoneNumber for c in contacts if c.phoneNumber]))

    return {
        "contact": {
            "primaryContatctId": primary.id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }