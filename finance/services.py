from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import FinancialRecord
import calendar


class FinancialSummaryService:
    """
    Service class for calculating financial summaries and analytics.
    """

    @staticmethod
    def get_dashboard_summary(user):
        """
        Get overall financial dashboard summary.
        All authenticated users see the same total (all records).
        
        Returns:
            dict: Contains total income, expenses, net balance, and record counts.
        """
        # All users see all records
        records = FinancialRecord.objects.filter(is_deleted=False)
        
        income_sum = records.filter(record_type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        expenses_sum = records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        net_balance = income_sum - expenses_sum

        record_counts_by_type = records.values('record_type').annotate(count=Count('id')).order_by('record_type')
        record_counts_by_category = records.values('category').annotate(count=Count('id')).order_by('category')

        types_dict = {item['record_type']: item['count'] for item in record_counts_by_type}
        categories_dict = {item['category']: item['count'] for item in record_counts_by_category}

        return {
            'total_income': income_sum,
            'total_expenses': expenses_sum,
            'net_balance': net_balance,
            'total_records': records.count(),
            'records_count_by_type': types_dict,
            'records_count_by_category': categories_dict,
        }

    @staticmethod
    def get_category_summary(user):
        """
        Get summary grouped by category (all records).
        
        Returns:
            list: List of category summaries with totals and counts.
        """
        # All users see all records
        records = FinancialRecord.objects.filter(is_deleted=False)
        
        category_summaries = records.values('category', 'record_type').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')

        # Add category display names
        category_map = {
            'salary': 'Salary',
            'bonus': 'Bonus',
            'investment': 'Investment',
            'food': 'Food',
            'transport': 'Transport',
            'utilities': 'Utilities',
            'entertainment': 'Entertainment',
            'healthcare': 'Healthcare',
            'education': 'Education',
            'other': 'Other',
        }

        result = []
        for summary in category_summaries:
            summary['category_display'] = category_map.get(summary['category'], summary['category'])
            summary['type'] = summary.pop('record_type')
            result.append(summary)

        return result

    @staticmethod
    def get_monthly_summary(user, months=12):
        """
        Get monthly summary for the past N months (all records).
        
        Args:
            user: The user object (not used, shows all records)
            months: Number of months to calculate (default 12)
            
        Returns:
            list: List of monthly summaries.
        """
        # All users see all records
        records = FinancialRecord.objects.filter(is_deleted=False)
        
        today = timezone.now().date()
        monthly_summaries = []

        for i in range(months):
            # Calculate the first day of the month
            first_day = today.replace(day=1) - timedelta(days=i * 30)
            first_day = first_day.replace(day=1)
            
            # Calculate the last day of the month
            last_day = first_day + timedelta(days=calendar.monthrange(first_day.year, first_day.month)[1] - 1)

            month_records = records.filter(date__gte=first_day, date__lte=last_day)

            income = month_records.filter(record_type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            expenses = month_records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            net = income - expenses

            monthly_summaries.append({
                'year': first_day.year,
                'month': first_day.month,
                'income': income,
                'expenses': expenses,
                'net': net,
            })

        return sorted(monthly_summaries, key=lambda x: (x['year'], x['month']))

    @staticmethod
    def get_recent_activity(user, limit=10):
        """
        Get recent financial records (all records).
        
        Args:
            user: The user object (not used, shows all records)
            limit: Number of recent records to return
            
        Returns:
            list: List of recent financial records with user info.
        """
        # All users see all records
        records = FinancialRecord.objects.filter(is_deleted=False)
        recent = records.order_by('-created_at')[:limit]

        return [
            {
                'id': record.id,
                'user': record.user.username,
                'amount': record.amount,
                'record_type': record.record_type,
                'category': record.category,
                'description': record.description,
                'date': record.date,
                'created_at': record.created_at,
            }
            for record in recent
        ]

    @staticmethod
    def get_record_statistics_for_period(user, start_date, end_date):
        """
        Get statistics for a specific date range (all records).
        
        Args:
            user: The user object (not used, shows all records)
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            dict: Statistics for the period.
        """
        # All users see all records
        records = FinancialRecord.objects.filter(
            is_deleted=False,
            date__gte=start_date,
            date__lte=end_date
        )

        income = records.filter(record_type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        expenses = records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_records': records.count(),
            'total_income': income,
            'total_expenses': expenses,
            'net_balance': income - expenses,
            'average_per_record': income + expenses / records.count() if records.count() > 0 else Decimal('0.00'),
        }
