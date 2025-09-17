from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_pet_name(animal_type: str = "Dog") -> str:
    # Component 1 - LLM
    llm = OpenAI(temperature=0.7)

    # Component 2 - Prompt Templat
    prompt_template_name = PromptTemplate(
        input_variables=['animal_type'],
        template="You are a {animal_type} name generator. You will be given a description of a pet and you will generate a list of 5 names for the pet."

    )

    # Component 3 - Chain
    # name_chain = prompt_template_name | llm Future
    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name)

    # Run the chain
    response = name_chain.invoke({"animal_type": animal_type})
    return response


if __name__ == "__main__":
    print("Running script...\n")

    animal = "Cat"
    pet_name = generate_pet_name(animal)

    print(f"Posible {animal}:")
    print(pet_name)
