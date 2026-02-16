from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Tuple
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


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        github_id=user.github_id,
        username=user.username,
        email=user.email,
        name=user.name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        location=user.location,
        company=user.company
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


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
        func.coalesce(project_count_subquery.c.project_count, 0).label('project_count')
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
        func.coalesce(project_count_subquery.c.project_count, 0).label('project_count')
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


def get_hackathons(db: Session, skip: int = 0, limit: int = 100):
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
    hackathons = db.query(
        models.Hackathon,
        func.coalesce(project_count_subquery.c.project_count, 0).label('project_count')
    ).outerjoin(
        project_count_subquery,
        models.Hackathon.id == project_count_subquery.c.hackathon_id
    ).offset(skip).limit(limit).all()
    
    # Convert to list of Hackathon objects with project_count added
    result = []
    for hackathon, project_count in hackathons:
        # Add project_count as an attribute
        hackathon.project_count = project_count
        result.append(hackathon)
    
    return result


def get_upcoming_hackathons(db: Session, skip: int = 0, limit: int = 100):
    from datetime import datetime
    return db.query(models.Hackathon).filter(
        models.Hackathon.start_date > datetime.utcnow()
    ).order_by(models.Hackathon.start_date).offset(skip).limit(limit).all()


def get_active_hackathons(db: Session, skip: int = 0, limit: int = 100):
    from datetime import datetime
    return db.query(models.Hackathon).filter(
        and_(
            models.Hackathon.start_date <= datetime.utcnow(),
            models.Hackathon.end_date >= datetime.utcnow(),
            models.Hackathon.is_active == True
        )
    ).offset(skip).limit(limit).all()


def create_hackathon(db: Session, hackathon: schemas.HackathonCreate, owner_id: int = None):
    hackathon_data = hackathon.dict()
    if owner_id is not None:
        hackathon_data['owner_id'] = owner_id
    db_hackathon = models.Hackathon(**hackathon_data)
    db.add(db_hackathon)
    db.commit()
    db.refresh(db_hackathon)
    return db_hackathon


def update_hackathon(db: Session, hackathon_id: int, hackathon_update: schemas.HackathonUpdate):
    db_hackathon = get_hackathon(db, hackathon_id)
    if db_hackathon:
        update_data = hackathon_update.dict(exclude_unset=True)
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


def update_team(db: Session, team_id: int, team_update: schemas.TeamCreate):
    db_team = get_team(db, team_id)
    if db_team:
        for key, value in team_update.dict().items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int):
    db_team = get_team(db, team_id)
    if db_team:
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

# Team Invitation CRUD operations


def get_team_invitation(db: Session, invitation_id: int):
    return db.query(models.TeamInvitation).filter(
        models.TeamInvitation.id == invitation_id
    ).first()


def get_pending_invitations_for_user(db: Session, user_id: int):
    from datetime import datetime
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
    if invitation and invitation.status == 'pending':
        invitation.status = 'accepted'
        # Add user to team
        add_team_member(db, invitation.team_id, invitation.invited_user_id)
        db.commit()
        db.refresh(invitation)
    return invitation


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
    # Check if already subscribed
    existing = get_newsletter_subscription(db, email)
    if existing:
        # Reactivate if previously unsubscribed
        if not existing.is_active:
            existing.is_active = True
            existing.unsubscribed_at = None
            db.commit()
            db.refresh(existing)
        return existing

    # Create new subscription
    db_subscription = models.NewsletterSubscription(
        email=email,
        source=source,
        is_active=True
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


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
