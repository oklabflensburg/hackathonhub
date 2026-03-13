import os
import unittest
from datetime import datetime, timedelta, timezone

os.environ.setdefault('DEBUG', 'false')
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from fastapi.testclient import TestClient

from app.core.auth import create_tokens
from app.core.database import SessionLocal, engine
from app.core.permissions import PERMISSION_CODES
from app.domain.models import Base, Hackathon, Permission, Role, RolePermission, Team, TeamMember, TeamReport, User, UserRole
from app.main import app


class RbacTeamReportTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

        self.owner = User(email='owner@example.com', username='owner', password_hash='secret', email_verified=True)
        self.reporter = User(email='reporter@example.com', username='reporter', password_hash='secret', email_verified=True)
        self.superuser = User(email='root@example.com', username='root', password_hash='secret', email_verified=True)
        self.stranger = User(email='stranger@example.com', username='stranger', password_hash='secret', email_verified=True)
        self.db.add_all([self.owner, self.reporter, self.superuser, self.stranger])
        self.db.commit()
        for user in (self.owner, self.reporter, self.superuser, self.stranger):
            self.db.refresh(user)

        hackathon = Hackathon(
            name='Hack',
            description='Test hackathon',
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=1),
            location='Flensburg',
            owner_id=self.owner.id,
            is_active=True,
            registration_open=True,
        )
        self.db.add(hackathon)
        self.db.commit()
        self.db.refresh(hackathon)
        self.hackathon = hackathon

        team = Team(name='Team Alpha', hackathon_id=hackathon.id, created_by=self.owner.id)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        self.team = team

        self.db.add(TeamMember(team_id=team.id, user_id=self.owner.id, role='owner'))
        self.db.add(TeamReport(team_id=team.id, reporter_id=self.reporter.id, reason='Spam links'))
        self.db.commit()

        self._seed_superuser_role()

        self.client = TestClient(app)
        self.owner_headers = self._auth_headers(self.owner)
        self.stranger_headers = self._auth_headers(self.stranger)
        self.superuser_headers = self._auth_headers(self.superuser)

    def tearDown(self):
        self.client.close()
        self.db.close()

    def _auth_headers(self, user: User):
        token = create_tokens(user.id, user.username)['access_token']
        return {'Authorization': f'Bearer {token}'}

    def _seed_superuser_role(self):
        super_role = Role(name='superuser', description='System role: superuser', is_system=True)
        assign_permission = Permission(code=PERMISSION_CODES['rbac_assign_roles'], description='assign roles', resource='rbac', action='assign_roles')
        view_permission = Permission(code=PERMISSION_CODES['rbac_view'], description='view roles', resource='rbac', action='view')
        report_permission = Permission(code=PERMISSION_CODES['team_reports_review'], description='review team reports', resource='team_reports', action='review')
        self.db.add_all([super_role, assign_permission, view_permission, report_permission])
        self.db.commit()
        self.db.refresh(super_role)
        self.db.refresh(assign_permission)
        self.db.refresh(view_permission)
        self.db.refresh(report_permission)
        self.db.add_all([
            RolePermission(role_id=super_role.id, permission_id=assign_permission.id),
            RolePermission(role_id=super_role.id, permission_id=view_permission.id),
            RolePermission(role_id=super_role.id, permission_id=report_permission.id),
            UserRole(user_id=self.superuser.id, role_id=super_role.id),
        ])
        self.db.commit()

    def test_hackathon_owner_can_list_team_reports(self):
        response = self.client.get(f'/api/hackathons/{self.hackathon.id}/team-reports', headers=self.owner_headers)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]['team']['name'], 'Team Alpha')
        self.assertEqual(payload[0]['reporter']['username'], 'reporter')

    def test_unrelated_user_cannot_list_team_reports(self):
        response = self.client.get(f'/api/hackathons/{self.hackathon.id}/team-reports', headers=self.stranger_headers)
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_assign_roles(self):
        role = Role(name='moderator', description='System role: moderator', is_system=True)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        response = self.client.patch(
            f'/api/admin/users/{self.stranger.id}/roles',
            headers=self.superuser_headers,
            json={'role_ids': [role.id]},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload[0]['name'], 'moderator')


if __name__ == '__main__':
    unittest.main()
