from groq import Groq

# GROQ API KEY

API_KEY = "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"

client = Groq(api_key=API_KEY)


# LLM FUNCTION

def ask_llm(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# SYNTHETIC EMPLOYEE DATA

employees = [
    {
        "name": "Rahul",
        "department": "Engineering",
        "mfa_enabled": True,
        "password_shared": False,
        "sensitive_data_personal_device": False
    },
    {
        "name": "Priya",
        "department": "HR",
        "mfa_enabled": False,
        "password_shared": False,
        "sensitive_data_personal_device": True
    },
    {
        "name": "Arjun",
        "department": "Finance",
        "mfa_enabled": True,
        "password_shared": True,
        "sensitive_data_personal_device": False
    },
    {
        "name": "Sneha",
        "department": "Marketing",
        "mfa_enabled": True,
        "password_shared": False,
        "sensitive_data_personal_device": False
    },
    {
        "name": "Vikram",
        "department": "Engineering",
        "mfa_enabled": False,
        "password_shared": True,
        "sensitive_data_personal_device": True
    }
]


# COMPLIANCE RULES

def check_compliance(employee):

    violations = []

    # Rule 1: MFA must be enabled
    if not employee["mfa_enabled"]:

        violations.append(
            "MFA is not enabled."
        )

    # Rule 2: Passwords must not be shared
    if employee["password_shared"]:

        violations.append(
            "Password sharing detected."
        )

    # Rule 3: Sensitive data must not be stored
    # on personal devices
    if employee["sensitive_data_personal_device"]:

        violations.append(
            "Sensitive data is stored on a personal device."
        )

    # Determine status
    if len(violations) == 0:

        status = "COMPLIANT"

    else:

        status = "NON-COMPLIANT"

    return {
        "name": employee["name"],
        "department": employee["department"],
        "status": status,
        "violations": violations
    }

# RUN COMPLIANCE CHECK

def evaluate_employees():

    results = []

    for employee in employees:

        result = check_compliance(employee)

        results.append(result)

    return results

# GENERATE COMPLIANCE REPORT

def generate_report(results):

    report_data = ""

    for result in results:

        report_data += f"""
Employee: {result["name"]}
Department: {result["department"]}
Status: {result["status"]}
Violations: {result["violations"]}
----------------------------------------
"""

    prompt = f"""
You are a Policy Compliance Reporting Agent.

Analyze the following compliance evaluation results.

Compliance Results:
{report_data}

Create a professional compliance report.

The report must contain:

1. Executive Summary
2. Total Employees Evaluated
3. Number of Compliant Employees
4. Number of Non-Compliant Employees
5. Employee-wise Findings
6. Recommended Remediation Actions

Important:

- Use only the information provided.
- Do not invent violations.
- Clearly distinguish compliant and non-compliant employees.
- Keep the report concise and professional.
"""

    return ask_llm(prompt)


# MAIN POLICY COMPLIANCE AGENT

def run_compliance_agent():

    print("\n==============================================")
    print("          POLICY COMPLIANCE AGENT")
    print("==============================================")


    # STEP 1: EVALUATE EMPLOYEES

    print("\n[1] Evaluating employee compliance...")

    results = evaluate_employees()


    # STEP 2: DISPLAY RULE-BASED RESULTS

    print("\n==============================================")
    print("          COMPLIANCE CHECK RESULTS")
    print("==============================================")

    for result in results:

        print(f"\nEmployee: {result['name']}")
        print(f"Department: {result['department']}")
        print(f"Status: {result['status']}")

        if result["violations"]:

            print("Violations:")

            for violation in result["violations"]:

                print(f"  - {violation}")

        else:

            print("Violations: None")


    # STEP 3: GENERATE AI REPORT

    print("\n==============================================")
    print("          AI COMPLIANCE REPORT")
    print("==============================================")

    report = generate_report(results)

    print("\n")
    print(report)


# PROGRAM START

if __name__ == "__main__":

    run_compliance_agent()