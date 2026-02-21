from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Optional, Tuple
from datetime import datetime
import models
import schemas

# User CRUD operations


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_github_id(db: Session, github_id: int):
    return db.query(models.User).filter(models.User.github_id == github_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def search_users(db: Session, username_query: str = None, limit: int = 10):
    """Search users by username (case-insensitive partial match)"""
    query = db.query(models.User)

    if username_query:
        # Case-insensitive partial match on username
        query = query.filter(models.User.username.ilike(f"%{username_query}%"))

    # Limit results and exclude current user from suggestions
    return query.limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        github_id=user.github_id,
        google_id=user.google_id,
        username=user.username,
        email=user.email,
        name=user.name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        location=user.location,
        company=user.company,
        password_hash=user.password_hash,
        auth_method=user.auth_method,
        email_verified=user.email_verified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_google_id(db: Session, google_id: str):
    return db.query(models.User).filter(
        models.User.google_id == google_id).first()


def update_user_google_id(db: Session, user_id: int, google_id: str):
    user = get_user(db, user_id)
    if user:
        user.google_id = google_id
        user.auth_method = "google"
        db.commit()
        db.refresh(user)
    return user


def update_user_last_login(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user


def update_user_password(db: Session, user_id: int, password_hash: str):
    user = get_user(db, user_id)
    if user:
        user.password_hash = password_hash
        user.auth_method = "email"
        db.commit()
        db.refresh(user)
    return user


def update_user_avatar(db: Session, user_id: int, avatar_url: str):
    user = get_user(db, user_id)
    if user:
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Update user profile information"""
    user = get_user(db, user_id)
    if not user:
        return None

    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def verify_user_email(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.email_verified = True
        db.commit()
        db.refresh(user)
    return user


# Refresh Token CRUD operations

def get_refresh_token(db: Session, token_id: str):
    return db.query(models.RefreshToken).filter(
        models.RefreshToken.token_id == token_id).first()


def create_refresh_token(db: Session, user_id: int, token_id: str,
                         expires_at, device_info=None, ip_address=None,
                         user_agent=None):
    try:
        db_token = models.RefreshToken(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token
    except Exception as e:
        # If we can't create the refresh token (e.g., missing columns),
        # log the error and return None instead of failing
        import logging
        logging.error(f"Failed to create refresh token: {e}")
        db.rollback()
        return None


def revoke_refresh_token(db: Session, token_id: str):
    token = get_refresh_token(db, token_id)
    if token:
        token.revoked = True
        token.revoked_at = datetime.utcnow()
        db.commit()
        db.refresh(token)
    return token


def revoke_all_user_refresh_tokens(db: Session, user_id: int):
    tokens = db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.revoked.is_(False)
    ).all()

    for token in tokens:
        token.revoked = True
        token.revoked_at = datetime.utcnow()

    db.commit()
    return len(tokens)


# Password Reset Token CRUD operations

def create_password_reset_token(db: Session, user_id: int, token: str,
                                expires_at):
    db_token = models.PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_password_reset_token(db: Session, token: str):
    return db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == token).first()


def mark_password_reset_token_used(db: Session, token_id: int):
    token = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.id == token_id).first()
    if token:
        token.used = True
        db.commit()
        db.refresh(token)
    return token


# Project CRUD operations


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()


def get_project_with_details(db: Session, project_id: int):
    return db.query(models.Project).options(
        joinedload(models.Project.owner),
        joinedload(models.Project.hackathon),
        joinedload(models.Project.votes),
        joinedload(models.Project.comments)
    ).filter(models.Project.id == project_id).first()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None
):
    query = db.query(models.Project)

    if search:
        # Perform case-insensitive search across multiple fields
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Project.title.ilike(search_pattern),
                models.Project.description.ilike(search_pattern),
                models.Project.technologies.ilike(search_pattern)
            )
        )

    return query.offset(skip).limit(limit).all()


def get_projects_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.owner_id == user_id
    ).offset(skip).limit(limit).all()


def get_projects_by_hackathon(db: Session, hackathon_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(
        models.Project.hackathon_id == hackathon_id
    ).offset(skip).limit(limit).all()


def get_projects_sorted_by_votes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).order_by(
        desc(models.Project.vote_score)
    ).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(
        **project.dict(),
        owner_id=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if db_project:
        for key, value in project_update.dict().items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        # First, get all comment IDs for this project
        comment_ids = db.query(models.Comment.id).filter(
            models.Comment.project_id == project_id
        ).all()
        comment_ids = [c[0] for c in comment_ids]

        if comment_ids:
            # Delete all comment votes for these comments
            db.query(models.CommentVote).filter(
                models.CommentVote.comment_id.in_(comment_ids)
            ).delete(synchronize_session=False)

            # Delete all comments for this project
            db.query(models.Comment).filter(
                models.Comment.project_id == project_id
            ).delete(synchronize_session=False)

        # Delete all votes for this project
        db.query(models.Vote).filter(
            models.Vote.project_id == project_id
        ).delete(synchronize_session=False)

        # Now delete the project
        db.delete(db_project)
        db.commit()
    return db_project


def increment_project_view_count(db: Session, project_id: int):
    """Increment the view count for a project"""
    db_project = get_project(db, project_id)
    if db_project:
        db_project.view_count = (db_project.view_count or 0) + 1
        db.commit()
        db.refresh(db_project)
    return db_project

# Hackathon CRUD operations


def get_hackathon(db: Session, hackathon_id: int):
    from sqlalchemy import func, select

    # Subquery to count projects per hackathon
    project_count_subquery = (
        select(
            models.Project.hackathon_id,
            func.count(models.Project.id).label('project_count')
        )
        .group_by(models.Project.hackathon_id)
        .subquery()
    )

    # Query hackathon with left join to get project count
    result = db.query(
        models.Hackathon,
        func.coalesce(project_count_subquery.c.project_count,
                      0).label('project_count')
    ).outerjoin(
        project_count_subquery,
        models.Hackathon.id == project_count_subquery.c.hackathon_id
    ).filter(models.Hackathon.id == hackathon_id).first()

    if result:
        hackathon, project_count = result
        # Add project_count as an attribute
        hackathon.project_count = project_count
        return hackathon
    return None


def get_hackathon_with_details(db: Session, hackathon_id: int):
    from sqlalchemy import func, select

    # Subquery to count projects per hackathon
    project_count_subquery = (
        select(
            models.Project.hackathon_id,
            func.count(models.Project.id).label('project_count')
        )
        .group_by(models.Project.hackathon_id)
        .subquery()
    )

    # Query hackathon with left join to get project count
    result = db.query(
        models.Hackathon,
        func.coalesce(project_count_subquery.c.project_count,
                      0).label('project_count')
    ).outerjoin(
        project_count_subquery,
        models.Hackathon.id == project_count_subquery.c.hackathon_id
    ).options(
        joinedload(models.Hackathon.projects),
        joinedload(models.Hackathon.teams),
        joinedload(models.Hackathon.registrations),
        joinedload(models.Hackathon.chat_rooms)
    ).filter(models.Hackathon.id == hackathon_id).first()

    if result:
        hackathon, project_count = result
        # Add project_count as an attribute
        hackathon.project_count = project_count
        return hackathon
    return None


def get_hackathons(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None
):
    from sqlalchemy import func, select

    # Subquery to count projects per hackathon
    project_count_subquery = (
        select(
            models.Project.hackathon_id,
            func.count(models.Project.id).label('project_count')
        )
        .group_by(models.Project.hackathon_id)
        .subquery()
    )

    # Query hackathons with left join to get project count
    query = db.query(
        models.Hackathon,
        func.coalesce(project_count_subquery.c.project_count,
                      0).label('project_count')
    ).outerjoin(
        project_count_subquery,
        models.Hackathon.id == project_count_subquery.c.hackathon_id
    )

    # Apply search filter if provided
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Hackathon.name.ilike(search_pattern),
                models.Hackathon.description.ilike(search_pattern),
                models.Hackathon.location.ilike(search_pattern)
            )
        )

    hackathons = query.offset(skip).limit(limit).all()

    # Convert to list of Hackathon objects with project_count added
    result = []
    for hackathon, project_count in hackathons:
        # Add project_count as an attribute
        hackathon.project_count = project_count
        result.append(hackathon)

    return result


def get_upcoming_hackathons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hackathon).filter(
        models.Hackathon.start_date > datetime.utcnow()
    ).order_by(models.Hackathon.start_date).offset(skip).limit(limit).all()


def get_active_hackathons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hackathon).filter(
        and_(
            models.Hackathon.start_date <= datetime.utcnow(),
            models.Hackathon.end_date >= datetime.utcnow(),
            models.Hackathon.is_active == True
        )
    ).offset(skip).limit(limit).all()


def create_hackathon(
    db: Session,
    hackathon: schemas.HackathonCreate,
    owner_id: int = None
):
    hackathon_data = hackathon.dict()
    # Remove fields that don't exist in the Hackathon model
    # project_count is a computed field in the schema, not a database column
    if 'project_count' in hackathon_data:
        del hackathon_data['project_count']
    if owner_id is not None:
        hackathon_data['owner_id'] = owner_id
    db_hackathon = models.Hackathon(**hackathon_data)
    db.add(db_hackathon)
    db.commit()
    db.refresh(db_hackathon)
    return db_hackathon


def update_hackathon(
    db: Session,
    hackathon_id: int,
    hackathon_update: schemas.HackathonUpdate
):
    db_hackathon = get_hackathon(db, hackathon_id)
    if db_hackathon:
        update_data = hackathon_update.dict(exclude_unset=True)
        # Remove fields that don't exist in the Hackathon model
        if 'project_count' in update_data:
            del update_data['project_count']
        for key, value in update_data.items():
            setattr(db_hackathon, key, value)
        db.commit()
        db.refresh(db_hackathon)
    return db_hackathon

# Hackathon Registration CRUD operations


def get_hackathon_registration(db: Session, registration_id: int):
    return db.query(models.HackathonRegistration).filter(
        models.HackathonRegistration.id == registration_id
    ).first()


def get_hackathon_registrations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HackathonRegistration).offset(skip).limit(limit).all()


def get_user_hackathon_registrations(db: Session, user_id: int):
    return db.query(models.HackathonRegistration).filter(
        models.HackathonRegistration.user_id == user_id
    ).all()


def get_hackathon_participants(db: Session, hackathon_id: int):
    return db.query(models.HackathonRegistration).filter(
        models.HackathonRegistration.hackathon_id == hackathon_id
    ).all()


def get_user_registration_for_hackathon(db: Session, user_id: int, hackathon_id: int):
    return db.query(models.HackathonRegistration).filter(
        models.HackathonRegistration.user_id == user_id,
        models.HackathonRegistration.hackathon_id == hackathon_id
    ).first()


def get_hackathon_participants_with_users(db: Session, hackathon_id: int):
    """Get hackathon participants with user details"""
    return db.query(
        models.User.id,
        models.User.username,
        models.User.name,
        models.User.avatar_url,
        models.HackathonRegistration.registered_at
    ).join(
        models.HackathonRegistration,
        models.User.id == models.HackathonRegistration.user_id
    ).filter(
        models.HackathonRegistration.hackathon_id == hackathon_id
    ).all()


def create_hackathon_registration(db: Session, registration: schemas.HackathonRegistrationCreate, user_id: int):
    # Check if user is already registered
    existing = get_user_registration_for_hackathon(
        db, user_id, registration.hackathon_id)
    if existing:
        return existing  # Already registered

    # Get the hackathon to update participant count
    hackathon = get_hackathon(db, registration.hackathon_id)
    if hackathon:
        # Increment participant count
        hackathon.participant_count = (hackathon.participant_count or 0) + 1

    db_registration = models.HackathonRegistration(
        **registration.dict(),
        user_id=user_id
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration


def delete_hackathon_registration(db: Session, registration_id: int):
    db_registration = get_hackathon_registration(db, registration_id)
    if db_registration:
        # Get the hackathon to update participant count
        hackathon = get_hackathon(db, db_registration.hackathon_id)
        if hackathon and hackathon.participant_count > 0:
            # Decrement participant count
            hackathon.participant_count -= 1

        db.delete(db_registration)
        db.commit()
    return db_registration

# Vote CRUD operations


def get_vote(db: Session, vote_id: int):
    return db.query(models.Vote).filter(models.Vote.id == vote_id).first()


def get_user_vote_for_project(db: Session, user_id: int, project_id: int):
    return db.query(models.Vote).filter(
        models.Vote.user_id == user_id,
        models.Vote.project_id == project_id
    ).first()


def get_project_votes(db: Session, project_id: int):
    return db.query(models.Vote).filter(
        models.Vote.project_id == project_id
    ).all()


def get_user_votes(db: Session, user_id: int):
    return db.query(models.Vote).filter(
        models.Vote.user_id == user_id
    ).all()


def create_vote(db: Session, vote: schemas.VoteCreate, user_id: int):
    # Check if user already voted on this project
    existing_vote = get_user_vote_for_project(db, user_id, vote.project_id)

    if existing_vote:
        # User already voted on this project
        if existing_vote.vote_type == vote.vote_type:
            # Same vote type - return existing vote without changes
            return existing_vote
        else:
            # Vote type changed (upvote to downvote or vice versa)
            # Update existing vote and adjust project counts
            project = get_project(db, vote.project_id)

            print(
                f"[DEBUG] Changing vote: user {user_id}, project {vote.project_id}")
            print(
                f"[DEBUG] Existing vote type: {existing_vote.vote_type}, new vote type: {vote.vote_type}")
            print(
                f"[DEBUG] Before change: up={project.upvote_count}, down={project.downvote_count}, score={project.vote_score}")

            # Remove old vote from counts
            if existing_vote.vote_type == 'upvote':
                project.upvote_count -= 1
                project.vote_score -= 1
                print(
                    f"[DEBUG] Removed upvote: up={project.upvote_count}, score={project.vote_score}")
            else:  # downvote
                project.downvote_count -= 1
                project.vote_score += 1
                print(
                    f"[DEBUG] Removed downvote: down={project.downvote_count}, score={project.vote_score}")

            # Add new vote to counts
            if vote.vote_type == 'upvote':
                project.upvote_count += 1
                project.vote_score += 1
                print(
                    f"[DEBUG] Added upvote: up={project.upvote_count}, score={project.vote_score}")
            else:  # downvote
                project.downvote_count += 1
                project.vote_score -= 1
                print(
                    f"[DEBUG] Added downvote: down={project.downvote_count}, score={project.vote_score}")

            print(
                f"[DEBUG] After change: up={project.upvote_count}, down={project.downvote_count}, score={project.vote_score}")

            # Update vote type
            existing_vote.vote_type = vote.vote_type
            db.commit()
            db.refresh(existing_vote)
            return existing_vote
    else:
        # User hasn't voted on this project before
        # Create new vote
        db_vote = models.Vote(
            **vote.dict(),
            user_id=user_id
        )
        db.add(db_vote)

        # Update project vote counts
        project = get_project(db, vote.project_id)

        print(
            f"[DEBUG] New vote: user {user_id}, project {vote.project_id}, type {vote.vote_type}")
        print(
            f"[DEBUG] Before: up={project.upvote_count}, down={project.downvote_count}, score={project.vote_score}")

        if vote.vote_type == 'upvote':
            project.upvote_count += 1
            project.vote_score += 1
            print(
                f"[DEBUG] After upvote: up={project.upvote_count}, score={project.vote_score}")
        else:  # downvote
            project.downvote_count += 1
            project.vote_score -= 1
            print(
                f"[DEBUG] After downvote: down={project.downvote_count}, score={project.vote_score}")

        db.commit()
        db.refresh(db_vote)
        return db_vote


def delete_vote(db: Session, user_id: int, project_id: int):
    vote = get_user_vote_for_project(db, user_id, project_id)
    if vote:
        # Update project vote counts
        project = get_project(db, project_id)

        print(
            f"[DEBUG] Deleting vote: user {user_id}, project {project_id}, type {vote.vote_type}")
        print(
            f"[DEBUG] Before delete: up={project.upvote_count}, down={project.downvote_count}, score={project.vote_score}")

        if vote.vote_type == 'upvote':
            project.upvote_count -= 1
            project.vote_score -= 1
            print(
                f"[DEBUG] After removing upvote: up={project.upvote_count}, score={project.vote_score}")
        else:  # downvote
            project.downvote_count -= 1
            project.vote_score += 1
            print(
                f"[DEBUG] After removing downvote: down={project.downvote_count}, score={project.vote_score}")

        db.delete(vote)
        db.commit()
    return vote

# File CRUD operations


def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()


def get_files_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.File).filter(
        models.File.uploaded_by == user_id
    ).offset(skip).limit(limit).all()


def create_file(db: Session, file: schemas.FileCreate, user_id: int, filepath: str):
    db_file = models.File(
        filename=file.filename,
        filepath=filepath,
        filetype=file.filetype,
        uploaded_by=user_id,
        file_size=file.file_size,
        mime_type=file.mime_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, file_id: int):
    db_file = get_file(db, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file

# Team CRUD operations


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_team_with_details(db: Session, team_id: int):
    return db.query(models.Team).options(
        joinedload(models.Team.members).joinedload(models.TeamMember.user),
        joinedload(models.Team.creator),
        joinedload(models.Team.hackathon)
    ).filter(models.Team.id == team_id).first()


def get_teams_by_hackathon(db: Session, hackathon_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Team).filter(
        models.Team.hackathon_id == hackathon_id
    ).offset(skip).limit(limit).all()


def get_user_teams(db: Session, user_id: int):
    return db.query(models.Team).join(
        models.TeamMember
    ).filter(
        models.TeamMember.user_id == user_id
    ).all()


def create_team(db: Session, team: schemas.TeamCreate, user_id: int):
    db_team = models.Team(
        **team.dict(),
        created_by=user_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    # Add creator as team owner
    db_team_member = models.TeamMember(
        team_id=db_team.id,
        user_id=user_id,
        role='owner'
    )
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team)

    return db_team


def update_team(db: Session, team_id: int, team_update: schemas.TeamUpdate):
    db_team = get_team(db, team_id)
    if db_team:
        update_data = team_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int):
    db_team = get_team(db, team_id)
    if db_team:
        # Delete all team members first (team_id has NOT NULL constraint)
        db.query(models.TeamMember).filter(
            models.TeamMember.team_id == team_id
        ).delete(synchronize_session=False)

        # Delete all team invitations
        db.query(models.TeamInvitation).filter(
            models.TeamInvitation.team_id == team_id
        ).delete(synchronize_session=False)

        # Set team_id to NULL for any projects referencing this team
        db.query(models.Project).filter(
            models.Project.team_id == team_id
        ).update(
            {models.Project.team_id: None},
            synchronize_session=False
        )

        # Get all chat rooms associated with this team
        chat_rooms = db.query(models.ChatRoom).filter(
            models.ChatRoom.team_id == team_id
        ).all()

        # For each chat room, delete related messages and participants
        for room in chat_rooms:
            # Delete chat messages for this room
            db.query(models.ChatMessage).filter(
                models.ChatMessage.room_id == room.id
            ).delete(synchronize_session=False)

            # Delete chat participants for this room
            db.query(models.ChatParticipant).filter(
                models.ChatParticipant.room_id == room.id
            ).delete(synchronize_session=False)

            # Delete the chat room
            db.delete(room)

        # Now delete the team
        db.delete(db_team)
        db.commit()
    return db_team

# Team Member CRUD operations


def get_team_member(db: Session, team_id: int, user_id: int):
    return db.query(models.TeamMember).filter(
        models.TeamMember.team_id == team_id,
        models.TeamMember.user_id == user_id
    ).first()


def add_team_member(db: Session, team_id: int, user_id: int, role: str = 'member'):
    # Check if already a member
    existing = get_team_member(db, team_id, user_id)
    if existing:
        return existing

    db_team_member = models.TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role
    )
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def remove_team_member(db: Session, team_id: int, user_id: int):
    team_member = get_team_member(db, team_id, user_id)
    if team_member:
        db.delete(team_member)
        db.commit()
    return team_member


def update_team_member(
    db: Session,
    team_id: int,
    user_id: int,
    team_member_update: schemas.TeamMemberUpdate
):
    team_member = get_team_member(db, team_id, user_id)
    if not team_member:
        return None

    # Update role if provided
    if team_member_update.role is not None:
        # Validate role value
        if team_member_update.role not in ['owner', 'member']:
            raise ValueError("Role must be 'owner' or 'member'")
        team_member.role = team_member_update.role

    db.commit()
    db.refresh(team_member)
    return team_member

# Team Invitation CRUD operations


def get_team_invitation(db: Session, invitation_id: int):
    return db.query(models.TeamInvitation).filter(
        models.TeamInvitation.id == invitation_id
    ).first()


def get_user_invitations(db: Session, user_id: int):
    """Get all pending invitations for a user"""
    return db.query(models.TeamInvitation).filter(
        models.TeamInvitation.invited_user_id == user_id,
        models.TeamInvitation.status == 'pending',
        or_(
            models.TeamInvitation.expires_at == None,
            models.TeamInvitation.expires_at > datetime.utcnow()
        )
    ).all()


def create_team_invitation(db: Session, invitation: schemas.TeamInvitationCreate, inviter_id: int):
    # Check if invitation already exists
    existing = db.query(models.TeamInvitation).filter(
        models.TeamInvitation.team_id == invitation.team_id,
        models.TeamInvitation.invited_user_id == invitation.invited_user_id,
        models.TeamInvitation.status == 'pending'
    ).first()
    if existing:
        return existing

    db_invitation = models.TeamInvitation(
        **invitation.dict(),
        invited_by=inviter_id
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation


def accept_team_invitation(db: Session, invitation_id: int):
    invitation = get_team_invitation(db, invitation_id)
    if not invitation:
        return None
    if invitation.status != 'pending':
        return None
    invitation.status = 'accepted'
    # Add user to team and get the team member object
    team_member = add_team_member(
        db, invitation.team_id, invitation.invited_user_id
    )
    db.commit()
    db.refresh(invitation)
    return team_member


def decline_team_invitation(db: Session, invitation_id: int):
    invitation = get_team_invitation(db, invitation_id)
    if invitation and invitation.status == 'pending':
        invitation.status = 'declined'
        db.commit()
        db.refresh(invitation)
    return invitation


# Comment CRUD operations

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()


def get_comments_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    from sqlalchemy.orm import joinedload

    return db.query(models.Comment).filter(
        models.Comment.project_id == project_id,
        models.Comment.parent_comment_id.is_(None)  # Top-level comments only
    ).options(
        joinedload(models.Comment.user),
        joinedload(models.Comment.replies).joinedload(models.Comment.user)
    ).order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()


def get_comment_with_replies(db: Session, comment_id: int):
    return db.query(models.Comment).options(
        joinedload(models.Comment.replies).joinedload(models.Comment.user),
        joinedload(models.Comment.user)
    ).filter(models.Comment.id == comment_id).first()


def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, project_id: int):
    db_comment = models.Comment(
        **comment.dict(),
        user_id=user_id,
        project_id=project_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentCreate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment_update.dict().items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment


def cleanup_corrupted_comment_votes(db: Session):
    """Delete any comment votes with NULL comment_id (should not exist)"""
    corrupted_votes = db.query(models.CommentVote).filter(
        models.CommentVote.comment_id.is_(None)
    ).all()
    for vote in corrupted_votes:
        db.delete(vote)
    if corrupted_votes:
        db.commit()
    return len(corrupted_votes)


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        # First, delete all votes for this comment
        # This prevents foreign key constraint violations
        votes = db.query(models.CommentVote).filter(
            models.CommentVote.comment_id == comment_id
        ).all()
        for vote in votes:
            db.delete(vote)

        # Also clean up any corrupted votes with NULL comment_id
        # Do this before flush to ensure they're gone
        cleanup_corrupted_comment_votes(db)

        # Flush to ensure votes are deleted before comment deletion
        db.flush()

        # Now delete the comment
        db.delete(db_comment)
        db.commit()
    return db_comment


def get_comment_vote(db: Session, comment_id: int, user_id: int):
    return db.query(models.CommentVote).filter(
        models.CommentVote.comment_id == comment_id,
        models.CommentVote.user_id == user_id
    ).first()


def create_comment_vote(db: Session, vote: schemas.CommentVoteCreate, user_id: int, comment_id: int):
    # Clean up any corrupted votes first
    cleanup_corrupted_comment_votes(db)

    # Check if vote already exists
    existing_vote = get_comment_vote(db, comment_id, user_id)

    if existing_vote:
        # Handle corrupted votes with NULL comment_id
        if existing_vote.comment_id is None:
            # Delete the corrupted vote and create a new one
            db.delete(existing_vote)
            db.commit()
            # Continue to create new vote below
        else:
            # Update existing vote
            existing_vote.vote_type = vote.vote_type
            db.commit()
            db.refresh(existing_vote)

            # Update comment vote counts
            comment = get_comment(db, comment_id)
            if comment:
                # Recalculate counts (simplified - in production would need proper logic)
                pass
            return existing_vote

    # Create new vote
    db_vote = models.CommentVote(
        **vote.dict(),
        user_id=user_id,
        comment_id=comment_id
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)

    # Update comment vote counts
    comment = get_comment(db, comment_id)
    if comment:
        if vote.vote_type == 'upvote':
            comment.upvote_count = (comment.upvote_count or 0) + 1
        elif vote.vote_type == 'downvote':
            comment.downvote_count = (comment.downvote_count or 0) + 1
        db.commit()

    return db_vote


def delete_comment_vote(db: Session, comment_id: int, user_id: int):
    vote = get_comment_vote(db, comment_id, user_id)
    if vote:
        # Update comment vote counts
        comment = get_comment(db, comment_id)
        if comment:
            if vote.vote_type == 'upvote':
                comment.upvote_count = max(0, (comment.upvote_count or 1) - 1)
            elif vote.vote_type == 'downvote':
                comment.downvote_count = max(
                    0, (comment.downvote_count or 1) - 1)
            db.commit()

        db.delete(vote)
        db.commit()
    return vote


# Newsletter Subscription CRUD operations

def get_newsletter_subscription(db: Session, email: str):
    return db.query(models.NewsletterSubscription).filter(
        models.NewsletterSubscription.email == email
    ).first()


def create_newsletter_subscription(
    db: Session,
    email: str,
    source: str = "website_footer"
):
    """Legacy function - use create_newsletter_subscription_atomic for atomic upsert"""
    return create_newsletter_subscription_atomic(db, email, source)[0]


def create_newsletter_subscription_atomic(
    db: Session,
    email: str,
    source: str = "website_footer",
    idempotency_key: Optional[str] = None
) -> Tuple[models.NewsletterSubscription, bool]:
    """
    Atomically create or update newsletter subscription.
    Returns (subscription, is_new) tuple where is_new is True if newly created.

    This function uses database-level atomic operations to prevent race conditions
    and duplicate subscriptions.
    """
    # First, try to get existing subscription
    existing = get_newsletter_subscription(db, email)

    if existing:
        # Subscription exists
        is_new = False

        # Reactivate if previously unsubscribed
        if not existing.is_active:
            existing.is_active = True
            existing.unsubscribed_at = None
            existing.source = source  # Update source
            if idempotency_key:
                # In a real implementation, we might store idempotency_key
                pass
            db.commit()
            db.refresh(existing)

        return existing, is_new

    # No existing subscription - create new one
    # Use database-level atomic insert with conflict handling
    try:
        db_subscription = models.NewsletterSubscription(
            email=email,
            source=source,
            is_active=True
        )
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription, True

    except Exception as e:
        # Handle race condition: another request might have created the subscription
        # between our check and the insert
        db.rollback()

        if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e).lower():
            # Subscription was created by another concurrent request
            # Fetch the newly created subscription
            existing = get_newsletter_subscription(db, email)
            if existing:
                return existing, False
            else:
                # This shouldn't happen, but if it does, retry once
                try:
                    db_subscription = models.NewsletterSubscription(
                        email=email,
                        source=source,
                        is_active=True
                    )
                    db.add(db_subscription)
                    db.commit()
                    db.refresh(db_subscription)
                    return db_subscription, True
                except Exception as e2:
                    # If still failing, raise the original error
                    db.rollback()
                    raise e
        else:
            # Some other error
            raise e


def unsubscribe_newsletter(db: Session, email: str):
    subscription = get_newsletter_subscription(db, email)
    if subscription and subscription.is_active:
        subscription.is_active = False
        subscription.unsubscribed_at = func.now()
        db.commit()
        db.refresh(subscription)
    return subscription


def get_active_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsletterSubscription).filter(
        models.NewsletterSubscription.is_active == True
    ).offset(skip).limit(limit).all()


# Notification CRUD operations

def get_notification_type(db: Session, type_key: str):
    """Get a notification type by its key."""
    return db.query(models.NotificationType).filter(
        models.NotificationType.type_key == type_key
    ).first()


def get_notification_types(db: Session):
    """Get all notification types."""
    return db.query(models.NotificationType).all()


def create_notification_type(db: Session, notification_type: schemas.NotificationTypeCreate):
    """Create a new notification type."""
    db_notification_type = models.NotificationType(**notification_type.dict())
    db.add(db_notification_type)
    db.commit()
    db.refresh(db_notification_type)
    return db_notification_type


def get_user_notification_preference(
    db: Session,
    user_id: int,
    notification_type: str,
    channel: str
):
    """Get a user's notification preference for a specific type and channel."""
    return db.query(models.UserNotificationPreference).filter(
        models.UserNotificationPreference.user_id == user_id,
        models.UserNotificationPreference.notification_type == notification_type,
        models.UserNotificationPreference.channel == channel
    ).first()


def get_user_notification_preferences(db: Session, user_id: int):
    """Get all notification preferences for a user."""
    return db.query(models.UserNotificationPreference).filter(
        models.UserNotificationPreference.user_id == user_id
    ).all()


def create_user_notification_preference(
    db: Session,
    user_id: int,
    notification_type: str,
    channel: str,
    enabled: bool = True
):
    """Create or update a user's notification preference."""
    # Check if preference already exists
    existing = get_user_notification_preference(db, user_id, notification_type, channel)
    
    if existing:
        # Update existing preference
        existing.enabled = enabled
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new preference
        db_preference = models.UserNotificationPreference(
            user_id=user_id,
            notification_type=notification_type,
            channel=channel,
            enabled=enabled
        )
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
        return db_preference


def update_user_notification_preference(
    db: Session,
    user_id: int,
    notification_type: str,
    channel: str,
    enabled: bool
):
    """Update a user's notification preference."""
    preference = get_user_notification_preference(db, user_id, notification_type, channel)
    if preference:
        preference.enabled = enabled
        db.commit()
        db.refresh(preference)
    return preference


def get_user_notifications(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False
):
    """Get notifications for a user."""
    query = db.query(models.UserNotification).filter(
        models.UserNotification.user_id == user_id
    )
    
    if unread_only:
        query = query.filter(models.UserNotification.read_at.is_(None))
    
    return query.order_by(models.UserNotification.created_at.desc()).offset(skip).limit(limit).all()


def create_user_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    data: dict = None,
    channel: str = "in_app"
):
    """Create a new user notification."""
    db_notification = models.UserNotification(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        data=data,
        channel=channel
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def mark_notification_as_read(db: Session, notification_id: int):
    """Mark a notification as read."""
    notification = db.query(models.UserNotification).filter(
        models.UserNotification.id == notification_id
    ).first()
    
    if notification and notification.read_at is None:
        notification.read_at = datetime.utcnow()
        db.commit()
        db.refresh(notification)
    
    return notification


def mark_all_notifications_as_read(db: Session, user_id: int):
    """Mark all notifications for a user as read."""
    notifications = db.query(models.UserNotification).filter(
        models.UserNotification.user_id == user_id,
        models.UserNotification.read_at.is_(None)
    ).all()
    
    for notification in notifications:
        notification.read_at = datetime.utcnow()
    
    db.commit()
    return len(notifications)


def get_push_subscription(db: Session, user_id: int, endpoint: str):
    """Get a push subscription for a user."""
    return db.query(models.PushSubscription).filter(
        models.PushSubscription.user_id == user_id,
        models.PushSubscription.endpoint == endpoint
    ).first()


def get_user_push_subscriptions(db: Session, user_id: int):
    """Get all push subscriptions for a user."""
    return db.query(models.PushSubscription).filter(
        models.PushSubscription.user_id == user_id
    ).all()


def create_push_subscription(
    db: Session,
    user_id: int,
    endpoint: str,
    keys: dict
):
    """Create a new push subscription."""
    # Check if subscription already exists
    existing = get_push_subscription(db, user_id, endpoint)
    
    # Extract keys from the dictionary
    p256dh = keys.get('p256dh') or keys.get('p256dh_key')
    auth = keys.get('auth') or keys.get('auth_key')
    
    if not p256dh or not auth:
        raise ValueError("Missing required keys: p256dh and auth")
    
    if existing:
        # Update existing subscription
        existing.p256dh = p256dh
        existing.auth = auth
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new subscription
        db_subscription = models.PushSubscription(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth
        )
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription


def delete_push_subscription(db: Session, user_id: int, endpoint: str):
    """Delete a push subscription."""
    subscription = get_push_subscription(db, user_id, endpoint)
    if subscription:
        db.delete(subscription)
        db.commit()
    return subscription
