import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useAccountContext } from 'frontend/contexts';
import TaskService from 'frontend/services/task.service';
import { Task, CreateTaskRequest, UpdateTaskRequest } from 'frontend/types/task';
import { TaskForm, TaskList } from 'frontend/components/task';
import { AsyncError } from 'frontend/types';

const Tasks: React.FC = () => {
  const { accountDetails } = useAccountContext();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const loadTasks = async (page: number = 1) => {
    if (!accountDetails?.id) return;
    
    setIsLoading(true);
    try {
      const response = await taskService.getTasks(accountDetails.id, page, 10);
      if (response.data) {
        setTasks(response.data.items);
        setTotalPages(response.data.total_pages);
        setTotalCount(response.data.total_count);
      }
      setCurrentPage(page);
    } catch (error) {
      const err = error as AsyncError;
      toast.error(err.message || 'Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  };

  const taskService = new TaskService();

  useEffect(() => {
    loadTasks();
  }, [accountDetails?.id]);

  const handleCreateTask = async (values: CreateTaskRequest) => {
    if (!accountDetails?.id) return;
    
    setIsLoading(true);
    try {
      await taskService.createTask(accountDetails.id, values);
      toast.success('Task created successfully');
      setShowForm(false);
      loadTasks(currentPage);
    } catch (error) {
      const err = error as AsyncError;
      toast.error(err.message || 'Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateTask = async (values: UpdateTaskRequest) => {
    if (!accountDetails?.id || !editingTask) return;
    
    setIsLoading(true);
    try {
      await taskService.updateTask(accountDetails.id, editingTask.id, values);
      toast.success('Task updated successfully');
      setEditingTask(null);
      loadTasks(currentPage);
    } catch (error) {
      const err = error as AsyncError;
      toast.error(err.message || 'Failed to update task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!accountDetails?.id) return;
    
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    
    setIsLoading(true);
    try {
      await taskService.deleteTask(accountDetails.id, taskId);
      toast.success('Task deleted successfully');
      loadTasks(currentPage);
    } catch (error) {
      const err = error as AsyncError;
      toast.error(err.message || 'Failed to delete task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handlePageChange = (page: number) => {
    loadTasks(page);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
            <p className="text-gray-600 mt-2">
              Manage your tasks ({totalCount} total)
            </p>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Add Task
          </button>
        </div>

        {(showForm || editingTask) && (
          <div className="mb-8">
            <TaskForm
              initialValues={editingTask ? { title: editingTask.title, description: editingTask.description } : undefined}
              onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
              onCancel={handleCancelForm}
              isLoading={isLoading}
              title={editingTask ? 'Edit Task' : 'Create New Task'}
              submitButtonText={editingTask ? 'Update Task' : 'Create Task'}
            />
          </div>
        )}

        <TaskList
          tasks={tasks}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
          isLoading={isLoading}
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      </div>
    </div>
  );
};

export default Tasks;
