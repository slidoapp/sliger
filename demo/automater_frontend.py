import streamlit as st
import subprocess
import os
import queue
from sliger import duplicate_presentation, main, jinjify, imagify
import redirect as rd

# Set the page title
st.set_page_config(page_title="Sliger", page_icon="🐯")

st.markdown("<h1 style='text-align: center;'>Slide of the Tiger - Sliger 🐯</h1>", unsafe_allow_html=True)

service_account_json = os.path.join(os.getcwd(), 'service_account.json')

account_uuid = st.text_input("Enter the account UUID (1/4)")

company_name = None
presentation_name = None
currency = None
presentation_id = None

if account_uuid:
    company_name = st.text_input("Enter the company name (2/4)")

if company_name:
    presentation_name = st.text_input("Enter the presentation name (3/4)")

if presentation_name:
    presentation_id = "1sROK5h0qjeyk0TLGCcCsq2MtCJCYDQO7O5f0EoaiDHY"

if presentation_id:
    currency = st.selectbox('Select the currency (4/4):', ["EUR €", "USD $", "GBP £"])

inputs_dict = {
    "account_uuid": account_uuid,
    "company_name": company_name,
    "presentation_name": presentation_name,
    "currency": currency
}

# Initialize slide_number, slide_id_image, and image_name
slide_number = None
slide_id_image = None
image_name = None


def run_command(service_account_json,
                presentation_id,
                action,
                slide_number,
                slide_id_image,
                image_name,
                output_queue):
    # Command to run
    cmd = [
        "python",
        "automater.py",
        "--creds-file",
        service_account_json,
        "--presentation-id",
        presentation_id,
        action,
    ]

    if action in ["jinjify", "imagify"]:
        cmd.append("--data")
        cmd.append(repr(inputs_dict))

    if slide_number is not None:
        cmd.extend(["--id", str(slide_number)])
    elif slide_id_image is not None and image_name is not None:
        cmd.extend(["--id", str(slide_id_image), "--img-path", f'img/{image_name}'])

    # Run the command
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)

    output_queue.put((result.stdout, result.stderr))


output_queue = queue.Queue()

if st.button('Launch') and presentation_id:
    st.write('Setting up state')

    with st.spinner('Running...'), st.expander('Output', expanded=False):
        with rd.stdout:
            main(service_account_json, presentation_id, "config.toml")

            st.write('Duplicating presentation')
            new_presentation_id = duplicate_presentation(f"Slido @ {inputs_dict['company_name']}")
            main(service_account_json, new_presentation_id, "config.toml")

            st.write('Jinjifying presentation')

            jinjify(inputs_dict)

            st.write('Imagifying presentation')
            imagify()

    st.markdown(f'Done! [View presentation](https://docs.google.com/presentation/d'
                f'/{new_presentation_id}/edit)')