import { useI18n } from 'vue-i18n'

/**
 * Composable für Hackathon-Stats-Labels
 * 
 * @example
 * ```typescript
 * const { labels } = useHackathonLabels()
 * ```
 */
export function useHackathonLabels() {
  const { t } = useI18n()

  const labels = {
    status: t('hackathons.details.status'),
    participants: t('hackathons.details.participants'),
    views: t('hackathons.details.views'),
    projects: t('hackathons.details.projects'),
    registrationDeadline: t('hackathons.details.registrationDeadline'),
    teams: t('hackathons.details.teams'),
    prizes: t('hackathons.details.prizes')
  }

  return {
    labels
  }
}