-- Intake lane mix
select
  triage_lane,
  count(*) as request_count,
  avg(business_value) as avg_business_value,
  avg(dependency_risk) as avg_dependency_risk,
  avg(acceptance_readiness) as avg_acceptance_readiness
from mobile_requests
group by 1
order by request_count desc;

-- Sprint-ready candidates
select
  request_id,
  request_name,
  platform_area,
  business_value,
  customer_impact,
  urgency,
  acceptance_readiness
from mobile_requests
where triage_lane = 'Actionable'
  and acceptance_readiness >= 80
order by business_value desc, customer_impact desc;

-- Dependency blockers that need owner resolution
select
  request_id,
  request_name,
  vendor_dependency,
  data_dependency,
  dependency_risk
from mobile_requests
where triage_lane = 'Blocked'
   or dependency_risk >= 75
order by dependency_risk desc;
