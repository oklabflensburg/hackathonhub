/**
 * Comment TypeScript Types for Atomic Design Components
 * 
 * This file defines all TypeScript interfaces and enums for comment components
 * Used across atoms, molecules, organisms, templates, and composables
 */

// ==================== ENUMS ====================

/**
 * Comment vote type
 */
export enum CommentVoteType {
  UPVOTE = 1,
  DOWNVOTE = -1,
  NONE = 0
}

/**
 * Comment sort options
 */
export enum CommentSortOption {
  NEWEST = 'newest',
  OLDEST = 'oldest',
  MOST_VOTED = 'most_voted',
  MOST_REPLIES = 'most_replies'
}

/**
 * Comment status
 */
export enum CommentStatus {
  ACTIVE = 'active',
  DELETED = 'deleted',
  HIDDEN = 'hidden',
  FLAGGED = 'flagged'
}

// ==================== INTERFACES ====================

/**
 * Base comment interface
 */
export interface Comment {
  id: string
  content: string
  userId: string
  userName: string
  userAvatarUrl: string | null
  userRole?: string | null
  parentId: string | null
  entityType: 'project' | 'hackathon' | 'team' | 'user'
  entityId: string
  voteCount: number
  userVote: CommentVoteType
  replyCount: number
  status: CommentStatus
  createdAt: string
  updatedAt: string
  deletedAt: string | null
  replies?: Comment[]
  isEdited: boolean
  metadata?: Record<string, any>
}

/**
 * Comment author information
 */
export interface CommentAuthor {
  id: string
  username: string
  displayName: string | null
  avatarUrl: string | null
  role?: string | null
  isVerified?: boolean
}

/**
 * Comment creation data
 */
export interface CommentCreateData {
  content: string
  parentId?: string | null
  entityType: 'project' | 'hackathon' | 'team' | 'user'
  entityId: string
  metadata?: Record<string, any>
}

/**
 * Comment update data
 */
export interface CommentUpdateData {
  content: string
  metadata?: Record<string, any>
}

/**
 * Comment vote data
 */
export interface CommentVoteData {
  commentId: string
  voteType: CommentVoteType
}

/**
 * Comment filter options
 */
export interface CommentFilterOptions {
  entityType?: 'project' | 'hackathon' | 'team' | 'user'
  entityId?: string
  userId?: string
  parentId?: string | null
  status?: CommentStatus[]
  sortBy?: CommentSortOption
  includeReplies?: boolean
  depth?: number
  page?: number
  pageSize?: number
}

/**
 * Comment pagination response
 */
export interface CommentPaginationResponse {
  comments: Comment[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
  hasMore: boolean
}

// ==================== COMPONENT PROPS ====================

/**
 * Comment item props
 */
export interface CommentItemProps {
  comment: Comment
  currentUserId?: string | null
  showActions?: boolean
  showReplies?: boolean
  depth?: number
  maxDepth?: number
  onReply?: (comment: Comment) => void
  onEdit?: (comment: Comment) => void
  onDelete?: (comment: Comment) => void
  onVote?: (commentId: string, voteType: CommentVoteType) => void
  onReport?: (comment: Comment) => void
}

/**
 * Comment list props
 */
export interface CommentListProps {
  comments: Comment[]
  loading?: boolean
  error?: string | null
  emptyMessage?: string
  currentUserId?: string | null
  showLoadMore?: boolean
  onLoadMore?: () => void
  onCommentSubmit?: (content: string, parentId?: string | null) => void
  onCommentVote?: (commentId: string, voteType: CommentVoteType) => void
  onCommentEdit?: (commentId: string, content: string) => void
  onCommentDelete?: (commentId: string) => void
}

/**
 * Comment form props
 */
export interface CommentFormProps {
  entityType: 'project' | 'hackathon' | 'team' | 'user'
  entityId: string
  parentId?: string | null
  placeholder?: string
  submitLabel?: string
  cancelLabel?: string
  showCancel?: boolean
  autoFocus?: boolean
  initialContent?: string
  onSubmit: (content: string) => Promise<void> | void
  onCancel?: () => void
  disabled?: boolean
  loading?: boolean
}

/**
 * Comment vote button props
 */
export interface CommentVoteButtonProps {
  commentId: string
  voteCount: number
  userVote: CommentVoteType
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  showCount?: boolean
  onVote: (commentId: string, voteType: CommentVoteType) => Promise<void> | void
}

/**
 * Comment actions dropdown props
 */
export interface CommentActionsDropdownProps {
  comment: Comment
  currentUserId?: string | null
  onEdit?: () => void
  onDelete?: () => void
  onReport?: () => void
  onShare?: () => void
  onCopyLink?: () => void
  disabled?: boolean
}

// ==================== COMPOSABLE RETURN TYPES ====================

/**
 * UseComments composable return type
 */
export interface UseCommentsReturn {
  comments: Ref<Comment[]>
  loading: Ref<boolean>
  error: Ref<string | null>
  totalCount: Ref<number>
  page: Ref<number>
  pageSize: Ref<number>
  sortOption: Ref<CommentSortOption>
  entityType: Ref<'project' | 'hackathon' | 'team' | 'user' | null>
  entityId: Ref<string | null>
  
  fetchComments: (options?: CommentFilterOptions) => Promise<void>
  fetchComment: (commentId: string) => Promise<Comment | null>
  createComment: (data: CommentCreateData) => Promise<Comment | null>
  updateComment: (commentId: string, data: CommentUpdateData) => Promise<Comment | null>
  deleteComment: (commentId: string) => Promise<boolean>
  voteComment: (commentId: string, voteType: CommentVoteType) => Promise<boolean>
  getReplies: (parentId: string) => Comment[]
  resetComments: () => void
}

// ==================== UTILITY TYPES ====================

/**
 * Comment thread props
 */
export interface CommentThreadProps {
  comment: Comment
  replies: Comment[]
  currentUserId?: string | null
  depth?: number
  maxDepth?: number
  showActions?: boolean
  onReply?: (comment: Comment) => void
  onVote?: (commentId: string, voteType: CommentVoteType) => void
}

/**
 * Comment sorting options props
 */
export interface CommentSortOptionsProps {
  sortOption: CommentSortOption
  onChange: (option: CommentSortOption) => void
  options?: Array<{
    value: CommentSortOption
    label: string
    icon?: string
  }>
}

// ==================== UTILITY CONSTANTS ====================

/**
 * Comment sort option labels
 */
export const COMMENT_SORT_LABELS: Record<CommentSortOption, string> = {
  [CommentSortOption.NEWEST]: 'Neueste',
  [CommentSortOption.OLDEST]: 'Älteste',
  [CommentSortOption.MOST_VOTED]: 'Meist gevotet',
  [CommentSortOption.MOST_REPLIES]: 'Meist Antworten'
}

/**
 * Comment vote type labels
 */
export const COMMENT_VOTE_LABELS: Record<CommentVoteType, string> = {
  [CommentVoteType.UPVOTE]: 'Upvote',
  [CommentVoteType.DOWNVOTE]: 'Downvote',
  [CommentVoteType.NONE]: 'Kein Vote'
}

/**
 * Comment status labels
 */
export const COMMENT_STATUS_LABELS: Record<CommentStatus, string> = {
  [CommentStatus.ACTIVE]: 'Aktiv',
  [CommentStatus.DELETED]: 'Gelöscht',
  [CommentStatus.HIDDEN]: 'Versteckt',
  [CommentStatus.FLAGGED]: 'Gemeldet'
}

/**
 * Comment status colors
 */
export const COMMENT_STATUS_COLORS: Record<CommentStatus, string> = {
  [CommentStatus.ACTIVE]: 'green',
  [CommentStatus.DELETED]: 'gray',
  [CommentStatus.HIDDEN]: 'yellow',
  [CommentStatus.FLAGGED]: 'red'
}