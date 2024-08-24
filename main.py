from browserbase import Browserbase
from playwright.async_api import async_playwright
import asyncio
import os


async def upload_and_verify_file(page, selector, file_path, input_name):
    file_input = await page.wait_for_selector(
        selector,
        state="attached",
        timeout=10000,
    )

    # Attempt to upload the file
    await file_input.set_input_files(file_path)

    # Verify the upload for this specific input
    uploaded_file_name = await file_input.evaluate("(el) => el.files[0]?.name")
    if uploaded_file_name:
        print(
            f"{input_name} file upload successful. Uploaded file: {uploaded_file_name}"
        )
    else:
        print(f"{input_name} file upload failed or no file was selected.")

    return uploaded_file_name


async def fill_and_verify_field(page, field_id, value):
    await page.fill(f"#{field_id}", value)
    filled_value = await page.input_value(f"#{field_id}")
    print(f"Successfully filled {field_id.capitalize()}: {filled_value}")
    return filled_value


async def type_dropdown_input(page, selector, input_text):
    await page.fill(selector, input_text)
    entered_value = await page.input_value(selector)

    print(f"Succesfully entered: {entered_value}")
    return entered_value


async def complete_form(applicant):
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.connect_over_cdp(
            f"wss://connect.browserbase.com?apiKey={os.getenv('BROWSERBASE_API_KEY')}"
        )
        page = await browser.new_page()
        await page.goto("https://job-boards.greenhouse.io/verkada/jobs/4477721007")

        # # Fill out and verify contact fields
        # await fill_and_verify_field(page, "first_name", applicant.first_name)
        # await fill_and_verify_field(page, "last_name", applicant.last_name)
        # await fill_and_verify_field(page, "email", applicant.email)
        # await fill_and_verify_field(page, "phone", applicant.phone)

        # # Upload resume
        # resume_file_path = os.path.abspath(applicant.resume_file_path)
        # await upload_and_verify_file(
        #     page,
        #     'input[type="file"][accept=".pdf,.doc,.docx,.txt,.rtf"]',
        #     resume_file_path,
        #     "Resume",
        # )

        # # set linkedin profile URL
        # await fill_and_verify_field(page, "question_6982466007", applicant.linkedin_url)

        # # Upload transcript
        # transcript_file_path = os.path.abspath(applicant.transcript_file_path)
        # await upload_and_verify_file(
        #     page,
        #     '#question_6982468007[type="file"]',
        #     transcript_file_path,
        #     "Transcript",
        # )

        # graduation year
        await type_dropdown_input(
            page,
            "#question_6982744007",
            applicant.graduation,
        )

        # GPA
        # await type_dropdown_input(
        #     page,
        #     "#question_6982504007",
        #     applicant.gpa,
        # )

        # ## School
        # await type_dropdown_input(
        #     page,
        #     "#school--0",
        #     applicant.school,
        # )

        # ## Degree
        # await type_dropdown_input(
        #     page,
        #     "#degree--0",
        #     applicant.degree,
        # )

        # ## Discipline
        # await type_dropdown_input(page, "#discipline--0", applicant.discipline)

        # # End month
        # await type_dropdown_input(page, "#end-month--0", applicant.graduation_month)

        # # End year
        # await type_dropdown_input(page, "#end-year--0", applicant.graduation_year)

        # all_fields_filled = await check_all_fields_filled(page, applicant)

        # if all_fields_filled:
        #     submit_button = page.locator("#submit")
        #     await submit_button.wait_for(state="visible")
        #     await submit_button.click()
        #     print("Form submitted successfully")
        # else:
        #     print("Form submission aborted: Some fields are empty")

        await browser.close()


async def check_all_fields_filled(page, applicant):
    fields_to_check = [
        ("#first_name", applicant.first_name),
        ("#last_name", applicant.last_name),
        ("#email", applicant.email),
        ("#phone", applicant.phone),
        ("#question_6982466007", applicant.linkedin_url),
        ("#question_6982744007", applicant.graduation),
        ("#question_6982504007", applicant.gpa),
        ("#school--0", applicant.school),
        ("#degree--0", applicant.degree),
        ("#discipline--0", applicant.discipline),
        ("#end-month--0", applicant.graduation_month),
        ("#end-year--0", applicant.graduation_year),
    ]

    for selector, expected_value in fields_to_check:
        value = await page.input_value(selector)
        if not value:
            print(f"Field {selector} is empty")
            return False

    # Check file uploads
    resume_uploaded = await page.evaluate(
        'document.querySelector(\'input[type="file"][accept=".pdf,.doc,.docx,.txt,.rtf"]\').files.length > 0'
    )
    transcript_uploaded = await page.evaluate(
        "document.querySelector('#question_6982468007[type=\"file\"]').files.length > 0"
    )

    if not resume_uploaded:
        print("Resume not uploaded")
        return False
    if not transcript_uploaded:
        print("Transcript not uploaded")
        return False

    return True


class Applicant:
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "john.doe@example.com"
        self.phone = "123-456-7890"
        self.resume_file_path = "JohnDoe_Resume.pdf"
        self.linkedin_url = "https://www.linkedin.com/in/andrewyng"
        self.transcript_file_path = (
            "JohnDoe_Resume.pdf"  # TODO: change to transcript PDF
        )
        self.graduation = "Aug - Dec 2025"
        self.gpa = "4.0"
        self.school = "Carnegie Mellon University"
        self.degree = "Bachelor's Degree"
        self.discipline = "Computer Science"
        self.graduation_month = "June"
        self.graduation_year = "2026"


andrew_ng = Applicant()
asyncio.run(complete_form(andrew_ng))
