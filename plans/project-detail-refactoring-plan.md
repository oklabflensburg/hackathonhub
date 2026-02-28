# Refactoring-Plan: Projekt-Detailseite (`projects/[id]/index.vue`)

## Aktueller Zustand
- **Datei**: `frontend3/app/pages/projects/[id]/index.vue`
- **Größe**: 34.216 Zeichen (ca. 778 Zeilen)
- **Refactoring-Status**: Teilweise refaktoriert
- **Verwendete Komponenten**: `ProjectHeader`, `TechnologyTags`, `ProjectLinks`, `ProjectStats`, `CreatorInfo`, `ProjectActions`

## Problembereiche

### 1. Kommentar-Sektion (Zeilen 63-330)
- **Größe**: ~267 Zeilen Inline-Code
- **Probleme**:
  - Komplexe Logik direkt in der Seite
  - Keine Wiederverwendbarkeit für andere Seiten
  - Gemischte Verantwortlichkeiten (UI, Logik, State)
  - Schwierig zu testen

### 2. Projekt-Bild Bereich (Zeilen 38-41)
- **Probleme**:
  - Inline HTML ohne Komponente
  - Keine Platzhalter-Logik
  - Kein Lazy-Loading

### 3. Beschreibungs-Bereich (Zeilen 43-49)
- **Probleme**:
  - Einfacher Bereich, könnte als Molecule extrahiert werden

### 4. Inline-Logik im Script-Teil
- **Probleme**:
  - Kommentar-bezogene Funktionen (`submitComment`, `editComment`, `deleteComment`, `voteComment`)
  - State-Management für Kommentare
  - Keine Trennung von Concerns

## Refactoring-Strategie

### Phase 1: Kommentar-System extrahieren

#### 1.1 Composable `useComments` erstellen
```typescript
// frontend3/app/composables/useComments.ts
export interface Comment {
  id: number;
  content: string;
  created_at: string;
  user_id: number;
  user: User;
  upvote_count: number;
  downvote_count: number;
  replies?: Comment[];
}

export function useComments(projectId: Ref<number | string>) {
  const comments = ref<Comment[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  async function fetchComments() { /* ... */ }
  async function postComment(content: string) { /* ... */ }
  async function editComment(commentId: number, content: string) { /* ... */ }
  async function deleteComment(commentId: number) { /* ... */ }
  async function voteComment(commentId: number, voteType: 'upvote' | 'downvote') { /* ... */ }
  
  return {
    comments,
    loading,
    error,
    fetchComments,
    postComment,
    editComment,
    deleteComment,
    voteComment
  };
}
```

#### 1.2 CommentItem Molecule erstellen
```vue
<!-- frontend3/app/components/molecules/CommentItem.vue -->
<template>
  <div class="comment-item">
    <Avatar :src="comment.user?.avatar_url" :alt="comment.user?.name" size="sm" />
    <div class="comment-content">
      <div class="comment-header">
        <span class="username">{{ comment.user?.name || 'Anonymous' }}</span>
        <span class="timestamp">{{ formatDate(comment.created_at) }}</span>
      </div>
      <p class="comment-text">{{ comment.content }}</p>
      <div class="comment-actions">
        <button @click="$emit('vote', comment.id, 'upvote')">↑ {{ comment.upvote_count }}</button>
        <button @click="$emit('vote', comment.id, 'downvote')">↓ {{ comment.downvote_count }}</button>
        <button v-if="editable" @click="$emit('edit', comment)">Edit</button>
        <button v-if="deletable" @click="$emit('delete', comment.id)">Delete</button>
        <button @click="$emit('reply', comment)">Reply</button>
      </div>
    </div>
  </div>
</template>
```

#### 1.3 CommentForm Molecule erstellen
```vue
<!-- frontend3/app/components/molecules/CommentForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="comment-form">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      :disabled="loading"
      rows="3"
      @keydown.ctrl.enter="handleSubmit"
    />
    <div class="form-actions">
      <Button type="button" variant="ghost" @click="$emit('cancel')">Cancel</Button>
      <Button type="submit" :loading="loading" :disabled="!content.trim()">
        {{ submitLabel }}
      </Button>
    </div>
  </form>
</template>
```

#### 1.4 CommentSection Organism erstellen
```vue
<!-- frontend3/app/components/organisms/CommentSection.vue -->
<template>
  <div class="comment-section">
    <h2 class="section-title">{{ title }} <span class="comment-count">{{ comments.length }}</span></h2>
    
    <!-- Add Comment Form -->
    <CommentForm
      v-if="showForm"
      v-model:content="newComment"
      :placeholder="formPlaceholder"
      :loading="postingComment"
      :submit-label="submitLabel"
      @submit="handleSubmitComment"
      @cancel="cancelComment"
    />
    
    <!-- Comments List -->
    <div v-if="loading" class="loading-state">
      <LoadingSpinner />
      <p>Loading comments...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <Button @click="fetchComments">Retry</Button>
    </div>
    
    <div v-else-if="comments.length === 0" class="empty-state">
      <p>No comments yet. Be the first to comment!</p>
    </div>
    
    <div v-else class="comments-list">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :editable="comment.user_id === currentUserId"
        :deletable="comment.user_id === currentUserId"
        @edit="handleEditComment"
        @delete="handleDeleteComment"
        @vote="handleVoteComment"
        @reply="handleReplyComment"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useComments } from '~/composables/useComments';

const props = defineProps({
  projectId: { type: [Number, String], required: true },
  currentUserId: { type: [Number, String], default: null },
  title: { type: String, default: 'Comments' },
  formPlaceholder: { type: String, default: 'Add a comment...' },
  submitLabel: { type: String, default: 'Post Comment' },
  showForm: { type: Boolean, default: true }
});

const emit = defineEmits(['commentAdded', 'commentUpdated', 'commentDeleted']);

const { comments, loading, error, fetchComments, postComment, editComment, deleteComment, voteComment } = 
  useComments(toRef(() => props.projectId));

// Initial fetch
onMounted(() => {
  fetchComments();
});

// Event handlers
const handleSubmitComment = async (content: string) => {
  const newComment = await postComment(content);
  emit('commentAdded', newComment);
};

const handleEditComment = async (comment: Comment, newContent: string) => {
  const updatedComment = await editComment(comment.id, newContent);
  emit('commentUpdated', updatedComment);
};

const handleDeleteComment = async (commentId: number) => {
  await deleteComment(commentId);
  emit('commentDeleted', commentId);
};

const handleVoteComment = async (commentId: number, voteType: 'upvote' | 'downvote') => {
  await voteComment(commentId, voteType);
};
</script>
```

### Phase 2: Projekt-Bild Komponente erstellen

#### 2.1 ProjectImage Molecule erstellen
```vue
<!-- frontend3/app/components/molecules/ProjectImage.vue -->
<template>
  <div class="project-image">
    <img
      :src="imageUrl"
      :alt="alt"
      :title="title"
      loading="lazy"
      @error="handleImageError"
      class="project-image__img"
    />
    <div v-if="showPlaceholder" class="project-image__placeholder">
      <div class="placeholder-content">
        <svg class="placeholder-icon" ... ></svg>
        <p class="placeholder-text">{{ placeholderText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: 'Project image' },
  title: { type: String, default: '' },
  placeholderText: { type: String, default: 'No image available' }
});

const imageUrl = computed(() => props.src || '');
const showPlaceholder = ref(!props.src);

const handleImageError = () => {
  showPlaceholder.value = true;
};
</script>
```

### Phase 3: Beschreibungs-Komponente erstellen

#### 3.1 ProjectDescription Molecule erstellen
```vue
<!-- frontend3/app/components/molecules/ProjectDescription.vue -->
<template>
  <Card :padding="'6'" class="project-description">
    <template #header>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">
        {{ title }}
      </h2>
    </template>
    <div class="prose dark:prose-invert max-w-none">
      <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">
        {{ content }}
      </p>
    </div>
  </Card>
</template>

<script setup lang="ts">
const props = defineProps({
  content: { type: String, required: true },
  title: { type: String, default: 'Description' }
});
</script>
```

### Phase 4: Integration in Projekt-Detailseite

#### 4.1 Schrittweise Ersetzung
1. **Projekt-Bild ersetzen** (Zeilen 38-41):
   ```vue
   <!-- Vorher -->
   <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden aspect-ratio-16-9">
     <img :src="projectImage" :alt="project.title" class="img-cover" />
   </div>
   
   <!-- Nachher -->
   <ProjectImage
     :src="projectImage"
     :alt="project.title"
     :title="project.title"
     class="rounded-xl shadow-lg"
   />
   ```

2. **Beschreibung ersetzen** (Zeilen 43-49):
   ```vue
   <!-- Vorher -->
   <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
     <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">{{ t('projects.detail.description') }}</h2>
     <div class="prose dark:prose-invert max-w-none">
       <p class="text-gray-700 dark:text-gray-300 whitespace-pre-line">{{ project.description }}</p>
     </div>
   </div>
   
   <!-- Nachher -->
   <ProjectDescription
     :content="project.description"
     :title="t('projects.detail.description')"
   />
   ```

3. **Kommentar-Sektion ersetzen** (Zeilen 63-330):
   ```vue
   <!-- Vorher -->
   <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
     <!-- 267 Zeilen Kommentar-Code -->
   </div>
   
   <!-- Nachher -->
   <CommentSection
     :project-id="project.id"
     :current-user-id="authStore.user?.id"
     :title="t('projects.detail.comments')"
     :form-placeholder="t('projects.comments.addCommentPlaceholder')"
     :submit-label="t('projects.comments.postComment')"
     @comment-added="handleCommentAdded"
     @comment-updated="handleCommentUpdated"
     @comment-deleted="handleCommentDeleted"
   />
   ```

#### 4.2 State Management anpassen
- Entferne Kommentar-bezogene State-Variablen aus der Seite:
  - `comments`, `commentsLoading`, `commentError`
  - `newComment`, `editingCommentId`, `editingCommentContent`
- Entferne Kommentar-bezogene Funktionen:
  - `fetchComments`, `submitComment`, `editComment`, `deleteComment`, `voteComment`
- Behalte nur Event-Handler für Seiten-spezifische Logik

#### 4.3 TypeScript-Typen aktualisieren
- Importiere `Comment` Interface aus `useComments`
- Aktualisiere Props für Event-Handler

### Phase 5: Testing

#### 5.1 Unit-Tests für neue Komponenten
- `CommentItem.test.ts`
- `CommentForm.test.ts`
- `CommentSection.test.ts`
- `ProjectImage.test.ts`
- `ProjectDescription.test.ts`

#### 5.2 Integrationstests für Projekt-Detailseite
- Teste, dass alle Komponenten korrekt gerendert werden
- Teste Kommentar-Funktionalität
- Teste Error-Handling
- Teste Responsive Design

#### 5.3 E2E-Tests (falls vorhanden)
- Teste vollständigen Kommentar-Workflow
- Teste Bild-Loading und Error-States
- Teste Navigation und Interaktionen

## Erfolgskriterien

### Für das Refactoring:
- [ ] Reduzierung der Seiten-Größe um mindestens 200 Zeilen
- [ ] Kommentar-Code komplett aus der Seite entfernt
- [ ] Keine Regressionen in Kommentar-Funktionalität
- [ ] Bessere Testbarkeit (isoliert testbare Komponenten)
- [ ] Wiederverwendbarkeit für andere Seiten (Hackathons, Teams)

### Für die neuen Komponenten:
- [ ] `CommentSection` kann in anderen Kontexten verwendet werden
- [ ] `ProjectImage` hat Platzhalter und Error-Handling
- [ ] `ProjectDescription` ist konsistent mit anderen Beschreibungs-Komponenten
- [ ] TypeScript-Typen sind korrekt und vollständig

## Risiken und Mitigation

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|--------|-------------------|------------|------------|
| Kommentar-Funktionalität bricht | Mittel | Hoch | Schrittweises Vorgehen, Tests nach jedem Schritt, Feature-Flag |
| Performance-Einbußen | Niedrig | Niedrig | Lazy-Loading von Kommentaren, Memoization |
| Design-Inkonsistenzen | Niedrig | Mittel | Design-Review, Tailwind-Klassen konsistent halten |
| TypeScript-Fehler | Mittel | Mittel | Strikte Typisierung, `strict: true` in tsconfig |

## Zeitplan

### Tag 1: Vorbereitung und Composable
- [ ] `useComments` Composable erstellen und testen
- [ ] Bestehende Kommentar-API integrieren
- [ ] TypeScript-Interfaces definieren

### Tag 2: CommentItem und CommentForm
- [ ] `CommentItem.vue` Molecule erstellen
- [ ] `CommentForm.vue` Molecule erstellen
- [ ] Unit-Tests schreiben
- [ ] In isoliertem Kontext testen

### Tag 3: CommentSection Organism
- [ ] `CommentSection.vue` Organism erstellen
- [ ] `ReplyThread.vue` Komponente (optional)
- [ ] Integration mit `useComments`
- [ ] Unit-Tests schreiben

### Tag 4: Projekt-Bild und Beschreibung
- [ ] `ProjectImage.vue` Molecule erstellen
- [ ] `ProjectDescription.vue` Molecule erstellen
- [ ] Unit-Tests schreiben

### Tag 5: Integration und Testing
- [ ] Schrittweise Integration in Projekt-Detailseite
- [ ] Manuelles Testing aller Funktionen
- [ ] Bug-Fixing und Optimierung
- [ ] Performance-Messung

## Nächste Schritte nach Abschluss

1. **Refactoring der Hackathon-Detailseite** mit ähnlichem Muster
2. **Refactoring der Team-Detailseite** 
3. **Vereinheitlichung aller Beschreibungs-Komponenten**
4. **Erstellung eines Design-Systems** basierend auf den neuen Atoms/Molecules