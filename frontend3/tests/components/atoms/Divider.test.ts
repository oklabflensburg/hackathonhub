import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Divider from '~/components/atoms/Divider.vue'

describe('Divider Atom', () => {
  it('renders a horizontal divider by default', () => {
    const wrapper = mount(Divider)
    
    expect(wrapper.find('hr').exists()).toBe(true)
    expect(wrapper.classes()).toContain('border-gray-200')
    expect(wrapper.classes()).toContain('dark:border-gray-700')
  })

  it('applies vertical class when vertical prop is true', () => {
    const wrapper = mount(Divider, {
      props: {
        vertical: true
      }
    })

    expect(wrapper.find('div').exists()).toBe(true)
    expect(wrapper.classes()).toContain('border-l')
    expect(wrapper.classes()).toContain('h-auto')
  })

  it('applies custom thickness class', () => {
    const wrapper = mount(Divider, {
      props: {
        thickness: 'thick'
      }
    })

    expect(wrapper.classes()).toContain('border-2')
  })

  it('applies custom color class', () => {
    const wrapper = mount(Divider, {
      props: {
        color: 'primary'
      }
    })

    expect(wrapper.classes()).toContain('border-primary-500')
    expect(wrapper.classes()).toContain('dark:border-primary-400')
  })

  it('applies custom spacing class', () => {
    const wrapper = mount(Divider, {
      props: {
        spacing: 'lg'
      }
    })

    expect(wrapper.classes()).toContain('my-8')
  })

  it('applies multiple custom props', () => {
    const wrapper = mount(Divider, {
      props: {
        vertical: true,
        thickness: 'thin',
        color: 'danger',
        spacing: 'sm'
      }
    })

    expect(wrapper.find('div').exists()).toBe(true)
    expect(wrapper.classes()).toContain('border-l')
    expect(wrapper.classes()).toContain('border')
    expect(wrapper.classes()).toContain('border-danger-500')
    expect(wrapper.classes()).toContain('dark:border-danger-400')
    expect(wrapper.classes()).toContain('mx-2')
  })

  it('applies custom class via class prop', () => {
    const wrapper = mount(Divider, {
      props: {
        class: 'custom-divider-class'
      }
    })

    expect(wrapper.classes()).toContain('custom-divider-class')
  })
})