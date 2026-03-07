// Molecules index file for atomic design exports
// This file exports all molecule components for easy importing

// Import all molecule components
import DateRangePicker from './DateRangePicker.vue'
import FileUpload from './FileUpload.vue'
import StatItem from './StatItem.vue'
import ProjectStats from './ProjectStats.vue'
import HackathonFilterBar from './HackathonFilterBar.vue'
import HackathonSearchInput from './HackathonSearchInput.vue'
import HackathonSortOptions from './HackathonSortOptions.vue'
import SearchBar from './SearchBar.vue'
import Pagination from './Pagination.vue'
import PageHeader from './PageHeader.vue'
import SelectedTags from './SelectedTags.vue'
import LoadingState from './LoadingState.vue'
import ErrorState from './ErrorState.vue'
import EmptyState from './EmptyState.vue'
import ProjectHeader from './ProjectHeader.vue'
import ProjectImage from './ProjectImage.vue'
import TechnologyTags from './TechnologyTags.vue'
import ProjectLinks from './ProjectLinks.vue'
import ProjectDescription from './ProjectDescription.vue'
import AuthForm from './AuthForm.vue'
import OAuthButtons from './OAuthButtons.vue'

// DateRangePicker - Date range selection molecule
export { default as DateRangePicker } from './DateRangePicker.vue'
export type { DateRangePickerProps, DateRange } from './DateRangePicker.vue'

// FileUpload - File upload molecule with drag & drop
export { default as FileUpload } from './FileUpload.vue'
export type { FileUploadProps, UploadFile } from './FileUpload.vue'

// StatItem - Statistics display molecule (existing)
export { default as StatItem } from './StatItem.vue'

// ProjectStats - Project statistics molecule
export { default as ProjectStats } from './ProjectStats.vue'

// HackathonFilterBar - Hackathon filtering molecule
export { default as HackathonFilterBar } from './HackathonFilterBar.vue'

// HackathonSearchInput - Hackathon search molecule
export { default as HackathonSearchInput } from './HackathonSearchInput.vue'

// HackathonSortOptions - Hackathon sorting molecule
export { default as HackathonSortOptions } from './HackathonSortOptions.vue'

// SearchBar - Search input molecule
export { default as SearchBar } from './SearchBar.vue'

// Pagination - Pagination molecule
export { default as Pagination } from './Pagination.vue'

// PageHeader - Page header molecule
export { default as PageHeader } from './PageHeader.vue'

// SelectedTags - Selected tags display molecule
export { default as SelectedTags } from './SelectedTags.vue'

// LoadingState - Loading state molecule
export { default as LoadingState } from './LoadingState.vue'

// ErrorState - Error state molecule
export { default as ErrorState } from './ErrorState.vue'

// EmptyState - Empty state molecule
export { default as EmptyState } from './EmptyState.vue'

// ProjectHeader - Project header molecule
export { default as ProjectHeader } from './ProjectHeader.vue'

// ProjectImage - Project image molecule
export { default as ProjectImage } from './ProjectImage.vue'

// TechnologyTags - Technology tags molecule
export { default as TechnologyTags } from './TechnologyTags.vue'

// ProjectLinks - Project links molecule
export { default as ProjectLinks } from './ProjectLinks.vue'

// ProjectDescription - Project description molecule
export { default as ProjectDescription } from './ProjectDescription.vue'

// AuthForm - Authentication form molecule
export { default as AuthForm } from './AuthForm.vue'

// OAuthButtons - OAuth provider buttons molecule
export { default as OAuthButtons } from './OAuthButtons.vue'

// Export all molecules as a single object for auto-import compatibility
export const molecules = {
  DateRangePicker,
  FileUpload,
  StatItem,
  ProjectStats,
  HackathonFilterBar,
  HackathonSearchInput,
  HackathonSortOptions,
  SearchBar,
  Pagination,
  PageHeader,
  SelectedTags,
  LoadingState,
  ErrorState,
  EmptyState,
  ProjectHeader,
  ProjectImage,
  TechnologyTags,
  ProjectLinks,
  ProjectDescription,
  AuthForm,
  OAuthButtons,
}

// Default export for module compatibility
export default molecules
