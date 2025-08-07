# Task Management Interface

This document describes the task management interface that has been built for the Flask-React template.

## Features

The task management interface provides the following CRUD operations:

- **Create Tasks**: Add new tasks with title and description
- **Read Tasks**: View all tasks with pagination support
- **Update Tasks**: Edit existing tasks
- **Delete Tasks**: Remove tasks with confirmation

## Components

### TaskForm
A reusable form component for creating and editing tasks with validation.

**Props:**
- `initialValues`: Initial form values (for editing)
- `onSubmit`: Callback function when form is submitted
- `onCancel`: Callback function when form is cancelled
- `isLoading`: Loading state
- `title`: Form title
- `submitButtonText`: Text for submit button

### TaskItem
Displays individual task cards with edit and delete actions.

**Props:**
- `task`: Task object to display
- `onEdit`: Callback function for edit action
- `onDelete`: Callback function for delete action
- `isLoading`: Loading state

### TaskList
Displays a grid of tasks with pagination controls.

**Props:**
- `tasks`: Array of tasks to display
- `onEdit`: Callback function for edit action
- `onDelete`: Callback function for delete action
- `isLoading`: Loading state
- `currentPage`: Current page number
- `totalPages`: Total number of pages
- `onPageChange`: Callback function for page changes

## API Integration

The interface uses the existing task CRUD APIs:

- `GET /api/accounts/{account_id}/tasks` - Get paginated tasks
- `GET /api/accounts/{account_id}/tasks/{task_id}` - Get single task
- `POST /api/accounts/{account_id}/tasks` - Create new task
- `PATCH /api/accounts/{account_id}/tasks/{task_id}` - Update task
- `DELETE /api/accounts/{account_id}/tasks/{task_id}` - Delete task

## Usage

1. **Access the Tasks Page**: Navigate to `/tasks` or click "Tasks" in the sidebar
2. **Create a Task**: Click "Add Task" button and fill out the form
3. **Edit a Task**: Click the edit icon on any task card
4. **Delete a Task**: Click the delete icon on any task card (confirmation required)
5. **Navigate Pages**: Use the pagination controls at the bottom

## Styling

The interface uses Tailwind CSS classes and includes:
- Responsive grid layout
- Hover effects and transitions
- Loading states
- Form validation with error messages
- Confirmation dialogs for destructive actions

## File Structure

```
src/apps/frontend/
├── components/task/
│   ├── task-form.tsx
│   ├── task-item.tsx
│   ├── task-list.tsx
│   └── index.ts
├── pages/tasks/
│   ├── tasks.tsx
│   └── index.tsx
├── services/
│   └── task.service.ts
└── types/
    └── task.ts
```

## Dependencies

- React 18
- Formik (for form handling)
- Yup (for validation)
- React Hot Toast (for notifications)
- Tailwind CSS (for styling)
- Axios (for API calls)
