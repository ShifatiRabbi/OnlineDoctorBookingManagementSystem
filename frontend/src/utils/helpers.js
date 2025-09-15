import { format, parseISO, isToday, isTomorrow, isThisWeek } from 'date-fns'

export const formatDate = (dateString, formatStr = 'PPP') => {
  if (!dateString) return ''
  try {
    return format(parseISO(dateString), formatStr)
  } catch {
    return dateString
  }
}

export const formatTime = (timeString) => {
  if (!timeString) return ''
  try {
    const [hours, minutes] = timeString.split(':')
    const hour = parseInt(hours)
    const period = hour >= 12 ? 'PM' : 'AM'
    const displayHour = hour % 12 || 12
    return `${displayHour}:${minutes} ${period}`
  } catch {
    return timeString
  }
}

export const getAppointmentStatusText = (status) => {
  const statusMap = {
    PENDING: 'Pending',
    CONFIRMED: 'Confirmed',
    CHECKED_IN: 'Checked In',
    CANCELLED: 'Cancelled',
    COMPLETED: 'Completed',
  }
  return statusMap[status] || status
}

export const getRelativeDate = (dateString) => {
  if (!dateString) return ''
  
  const date = parseISO(dateString)
  
  if (isToday(date)) return 'Today'
  if (isTomorrow(date)) return 'Tomorrow'
  if (isThisWeek(date)) return format(date, 'EEEE')
  
  return formatDate(dateString, 'MMM dd')
}

export const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}