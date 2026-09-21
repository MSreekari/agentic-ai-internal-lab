from groq import Groq

API_KEY = "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"

client = Groq(api_key=API_KEY)

def ask(prompt):

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

# AGENT 1: LEAD GENERATION

def lead_generation_agent(product, industry):

    prompt = f"""
You are a Lead Generation Agent.

Your task is to identify potential customers
for the given product.

Product:
{product}

Target Industry:
{industry}

Generate 3 fictional example companies.

For each company provide:

Company Name:
Industry:
Company Size:
Potential Need:
Reason why this company could be a good lead:

Return the results as a numbered list.
"""

    return ask(prompt)

# AGENT 2: LEAD QUALIFICATION

def qualification_agent(leads, product):

    prompt = f"""
You are a Lead Qualification Agent.

Your task is to evaluate potential customers
for the following product.

Product:
{product}

Potential Leads:
{leads}

For each lead:

1. Give a qualification score from 1 to 10.
2. Explain the reason for the score.
3. Decide whether the lead is QUALIFIED or NOT QUALIFIED.

Consider:

- Relevance of the industry
- Company size
- Potential need for the product
- Potential business value

Only leads with a score of 7 or higher
should be marked as QUALIFIED.

Return the results clearly.
"""

    return ask(prompt)


# AGENT 3: EMAIL GENERATION

def email_agent(qualified_leads, product):

    prompt = f"""
You are an SDR Email Agent.

Your task is to create personalized outreach
emails for QUALIFIED leads.

Product:
{product}

Qualified Leads:
{qualified_leads}

For every QUALIFIED lead:

1. Create a short subject line.
2. Write a professional personalized email.
3. Explain how the product could help the company.
4. Include a simple call to action.
5. Keep the email under 120 words.

Do NOT create emails for leads marked
NOT QUALIFIED.

Return each email separately.
"""

    return ask(prompt)


# MAIN SDR SYSTEM

def run_sdr_system():

    print("\n======================================")
    print("       MULTI-AGENT SDR SYSTEM")
    print("======================================")

    product = input(
        "\nEnter the product/service: "
    )

    industry = input(
        "Enter the target industry: "
    )


    # LEAD GENERATION

    print("\n======================================")
    print("       LEAD GENERATION AGENT")
    print("======================================")

    leads = lead_generation_agent(
        product,
        industry
    )

    print("\nGenerated Leads:\n")
    print(leads)


    # LEAD QUALIFICATION

    print("\n======================================")
    print("       LEAD QUALIFICATION AGENT")
    print("======================================")

    qualified_leads = qualification_agent(
        leads,
        product
    )

    print("\nQualification Results:\n")
    print(qualified_leads)

    # EMAIL GENERATION

    print("\n======================================")
    print("       EMAIL GENERATION AGENT")
    print("======================================")

    emails = email_agent(
        qualified_leads,
        product
    )

    print("\nGenerated Emails:\n")
    print(emails)


# PROGRAM START

if __name__ == "__main__":
    run_sdr_system()