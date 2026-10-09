
from agents.adverse_event_agent import adverse_event_agent
from agents.trial_data_agent import trial_data_agent
from agents.literature_research_agent import literature_research_agent
from agents.compound_similarity_agent import compound_similarity_agent
from agents.report_writer_agent import report_writer_agent


print("\nPharmaSense AI - Report Writer Integration Test")
print("=" * 60)


question = "Provide a report for compound CMP-0055."


print("\nRunning Literature Research Agent...")

literature_data = literature_research_agent(
    "CMP-0055",
    top_k=5
)


print("\nRunning Compound Similarity Agent...")

compound_data = compound_similarity_agent(
    "CMP-0055",
    top_n=5
)
print("\nRunning Trial Data Analyst Agent...")

trial_data = trial_data_agent(
    question
)


print("\nRunning Adverse Event Agent...")

adverse_event_data = adverse_event_agent(
    "TRL-0037"
)


print("\nRunning Report Writer Agent...")

final_report = report_writer_agent(
    question=question,
    trial_data=trial_data,
    literature_data=literature_data,
    compound_similarity_data=compound_data,
    adverse_event_data=adverse_event_data
)


print("\nFINAL REPORT")
print("=" * 60)

print(final_report)

