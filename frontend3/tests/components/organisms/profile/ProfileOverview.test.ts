import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ProfileOverview from '~/components/organisms/profile/ProfileOverview.vue'

describe('ProfileOverview Organism', () => {
  const mockUser = {
    id: '1',
    firstName: 'Max',
    lastName: 'Mustermann',
    email: 'max.mustermann@example.com',
    avatarUrl: 'https://example.com/avatar.jpg',
    bio: 'Software Developer with passion for Vue.js',
    location: 'Berlin, Germany',
    website: 'https://maxmustermann.dev',
    githubUsername: 'maxmustermann',
    twitterUsername: 'max_dev',
    createdAt: '2024-01-01T10:00:00Z',
    updatedAt: '2024-05-01T14:30:00Z',
    role: 'user',
    isVerified: true,
    isActive: true,
    emailNotifications: true,
    pushNotifications: false,
    language: 'de',
    timezone: 'Europe/Berlin'
  }

  const mockStats = {
    projectCount: 12,
    teamCount: 3,
    hackathonCount: 5,
    commentCount: 42,
    voteCount: 128,
    followerCount: 24,
    followingCount: 18,
    averageRating: 4.5,
    totalPoints: 1500
  }

  it('renders user information correctly', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: false
      }
    })

    expect(wrapper.text()).toContain('Max Mustermann')
    expect(wrapper.text()).toContain('max.mustermann@example.com')
    expect(wrapper.text()).toContain('Software Developer with passion for Vue.js')
    expect(wrapper.text()).toContain('Berlin, Germany')
    expect(wrapper.text()).toContain('maxmustermann.dev')
  })

  it('displays edit button for current user', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: true
      }
    })

    expect(wrapper.find('button').exists()).toBe(true)
    expect(wrapper.text()).toContain('Profil bearbeiten')
    expect(wrapper.text()).toContain('Einstellungen')
  })

  it('hides edit button for non-current user', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: false
      }
    })

    // Should not show edit buttons for other users
    expect(wrapper.text()).not.toContain('Profil bearbeiten')
    expect(wrapper.text()).not.toContain('Einstellungen')
  })

  it('displays stats when provided', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        stats: mockStats,
        isCurrentUser: false
      }
    })

    expect(wrapper.text()).toContain('12')
    expect(wrapper.text()).toContain('Projekte')
    expect(wrapper.text()).toContain('3')
    expect(wrapper.text()).toContain('Teams')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('Hackathons')
    expect(wrapper.text()).toContain('128')
    expect(wrapper.text()).toContain('Votes')
  })

  it('shows default values when stats are not provided', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: false
      }
    })

    expect(wrapper.text()).toContain('0')
    expect(wrapper.text()).toContain('Projekte')
    expect(wrapper.text()).toContain('0')
    expect(wrapper.text()).toContain('Teams')
    expect(wrapper.text()).toContain('0')
    expect(wrapper.text()).toContain('Hackathons')
    expect(wrapper.text()).toContain('0')
    expect(wrapper.text()).toContain('Votes')
  })

  it('displays social links when available', () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: false
      }
    })

    const githubLink = wrapper.find('a[href="https://github.com/maxmustermann"]')
    const twitterLink = wrapper.find('a[href="https://twitter.com/max_dev"]')

    expect(githubLink.exists()).toBe(true)
    expect(twitterLink.exists()).toBe(true)
  })

  it('hides social links when not available', () => {
    const userWithoutSocial = {
      ...mockUser,
      githubUsername: undefined,
      twitterUsername: undefined
    }

    const wrapper = mount(ProfileOverview, {
      props: {
        user: userWithoutSocial,
        isCurrentUser: false
      }
    })

    const githubLink = wrapper.find('a[href*="github.com"]')
    const twitterLink = wrapper.find('a[href*="twitter.com"]')

    expect(githubLink.exists()).toBe(false)
    expect(twitterLink.exists()).toBe(false)
  })

  it('emits edit-profile event when edit button is clicked', async () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: true
      }
    })

    const editButton = wrapper.findAll('button')[0]
    await editButton.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('edit-profile')
  })

  it('emits settings event when settings button is clicked', async () => {
    const wrapper = mount(ProfileOverview, {
      props: {
        user: mockUser,
        isCurrentUser: true
      }
    })

    const settingsButton = wrapper.findAll('button')[1]
    await settingsButton.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('settings')
  })

  it('uses default avatar when avatarUrl is not provided', () => {
    const userWithoutAvatar = {
      ...mockUser,
      avatarUrl: undefined
    }

    const wrapper = mount(ProfileOverview, {
      props: {
        user: userWithoutAvatar,
        isCurrentUser: false
      }
    })

    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe('/default-avatar.png')
  })

  it('displays display name correctly when first and last name are missing', () => {
    const userWithoutName = {
      ...mockUser,
      firstName: '',
      lastName: ''
    }

    const wrapper = mount(ProfileOverview, {
      props: {
        user: userWithoutName,
        isCurrentUser: false
      }
    })

    // Should show email username part
    expect(wrapper.text()).toContain('max.mustermann')
  })
})