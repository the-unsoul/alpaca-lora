sample = 'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. \n\n### Instruction:\n Generate 3 questions for the following passage \n\n### Input:\n Within Flowbird. Smart city multi-services kiosque is a terminal which replaced a Parking meter ("horodateur" in French). The difference between a parking meter and a smart city multi-services kiosque is that last one offers the following functions besides the possibility to pay for parking services: maps, timetables, guides, advertisements, tickets for events, coupons which offer discounts in shops etc. Examples of Smart city mult-services kiosques are: StradaPAL and T-PAL module. \n\n### Response:\n 1.   What are some examples of additional functions offered by smart city multi-services kiosques beyond just parking?\n2.   How do these additional functions benefit users compared to traditional parking meters?\n3.   Are there any potential drawbacks or limitations to offering such a wide range of services through a single kiosque?'

def extract_question(text: str):
    splitted = text.split('### Response:\n')
    return splitted[1].strip()

output = extract_question(sample)

print(output)