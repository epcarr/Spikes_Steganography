from bakery import assert_equal
from dataclasses import dataclass
from PIL import Image as PIL_Image 
from drafter import *
import os

hide_debug_information()
set_website_title("Spike's Silly Doggo Site")
set_website_framed(False) 

set_website_style("none")
add_website_css("""
body {
    background-color:#bfb9b9 ;
    font-size: 20px;
}

.name-box {
    background-color: pink;
    float: right;
}
""")

PAGE_SPECIFIC_STYLE = """<style>
.name-box {
    margin: 10px;
}
</style>
""",


@dataclass
class State:
    message: str
    pup_coins: int
    image: PIL_Image
    decoded_msg: str
    encoded_msg:str
    msg_hist:list[str]
    error_msg:str
    spikes_coins:int
    encoded_img:PIL_Image


@route
def index(state: State) -> Page:
    '''
    Description: This is the main page of the website, from here you
                can navigate through the various routes such as the
                encoder and decoder, aswell as looking at information
                about Spike himself and the programmer.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    
    return Page(state, ["Welcome to Spike's Silly Doggo Website!",
        "Send Puppers with messages to your buddies!!",
        Image(url='Spike_2.png',width=300, height=425),
        Button("Import Pupper", import_pupper),
        Button("Export Pupper", export_pupper),
        Button("How-to", how_to),
        Button("Pup Coins", pup_coins),
        Button("Meet Spike", our_creator),
        Button("Message History", msg_history)
        ])

@route
def how_to(state:State)-> Page:
    '''
    Description: This page leads to a description of how to work the
                 the encoder on this website.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
   
    return Page(state,[ "How to Guides:",
    Button("How to send encoded images?", how_to_send),
    Button("How to decode images?", how_to_view),
    Button("Home", index)
                        ])
@route
def how_to_send(state:State)->Page:
    '''
    Description: This page leads to a description of how to work the
                 the encoder on this website.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, ["If 'Send Pupper' selected:",
    "Step 1: You will be prompted to upload a picture of a pupper.",
    "Step 2: Once photo is uploaded, type message you want to send.",
    "Step 3: Download the new image of pupper with message.",
    "Step 4: Success! You earned a Pup coin!!",
    Button("Back", how_to)
    ])

@route
def how_to_view(state:State)->Page:
    '''
    Description: This page leads to a description of how to work the
                 the decoder on this website.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, ["If 'Import Pupper' selected:",
    "Step 1: You will be prompted to upload this image",
    "Note: You can view the image by clicking 'Display'",
    "Step 2: You can decode you message by clicking 'decode'",
    "Step 3: View your silly decoded message!",
    "Step 4: Success! You earned a Pup coin!!",
    Button("Back", how_to)
    ])

@route
def pup_coins(state:State)->Page:
    '''
    Description: This function allows you to
                 view how many pup coins you have.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, ["You have " + str(state.pup_coins) + " pup coins",
            "Send or Receive some Puppers for pup coins!! :)",
            Button("Home", index) ])

@route
def our_creator(state:State)->Page:
    '''
    Description: This is a page that gives you a brief background
                of Spike and the creator of the program. There is
                the option to give him a pup coin, which will take you
                to another page, depending if you have pup coins or not
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, [""" Meet Spike, the creator's beloved Rottweiler,
                        who is the main face of thie website and inspiration
                        for the Silly Doggo Website.""",
                        Image("me&spike.png",width=200,height=325),
                        "Would you like to give spike a pup coin?",
                        Button("Yes", give_pup_coin),
                        Button("No",index),
                        Button("Home", index),
                        
                        ])

@route
def give_pup_coin(state:State)->Page:
    '''
    Description: This function allows you to give spike a
                pup coin, making him happy. If you do not
                have any pup coins, an error message appears.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    result = None
    if state.pup_coins > 0:
        state.pup_coins -= 1
        state.spikes_coins +=1
        
        result = Page(state, ["Yay!! Spike is happy!!",
                            Image(url="happyspike.png", width= 300, height= 425),
                            "He thanks you for your kindness.",
                            Button("Home", index),
                            ])
        
        return result
                                                      
    else:
        state.error_msg= "Whoops, you dont have any pup coins :("
        result= Page(state, [state.error_msg,
                            Image(url="pensivespike.png",width=300,height=425),
                            "Send or receive messages to earn pup coins!!",
                            Button("Home",index)
                            ])
                            
        
        return result
    
    return result                   
                        
                        
@route
def import_pupper(state:State)->Page:
    '''
    Description: This is the main page of the decoding function,
                 here you can upload an image with a hidden message
                and then you can click "display" to show the image to verify
                if it's right.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, ["What would you like to import?",
           FileUpload("new_image", accept="image/png"),
           Button("Display", display_image),
           Button("Back", index)
            ])


@route
def display_image(state:State, new_image:bytes) -> Page:
    '''
    Description: This function displays the uploaded image to
                 the user and then asks if the user wants it
                 to decode the image.
    
    Args:
    - state: State
    - new_image: bytes
    
    
    
    Returns:
    - Page
    
    '''
    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')

    return Page(state, [
        Image(state.image, width=300,height=425),
        Button("Decode", decode_message),
        Button("Back", import_pupper)
        ])

@route
def decode_message(state:State)->Page:
    '''
    Description: This message decodes the PIL_Image and displays the
                decoded messasge to you. You also earn a pup coin.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    
    
    
    
    green_vals= get_color_values(state.image,1)
    decoded_message= get_encoded_message(green_vals)   
    state.decoded_msg = decoded_message
    state.pup_coins += 1
    
    return Page(state, ["Heres your message:",
                        state.decoded_msg,
                        "You earned one pup coin!",
                        Button("Home", index)
                        ])


@route
def export_pupper(state:State)->Page:
    '''
    Description: This is the hub for uploading an image so you can encode
                a message in it. It will ask you what you message you would like to embed
                inside the image.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    return Page(state, ["What would you like to send?",
                        FileUpload("new_image", accept="image/png"),
                        TextBox("new_message", "Type your message here!"),
                        Button("View Pupper!",encoding_process),
                        Button("Back", index)
                        ])

@route
def encoding_process(state:State, new_message:str, new_image:bytes)->Page:
    '''
    Description: This function takes the message and image and encodes this
                 message inside it. It later updates the State and returns
                 the image with the embedded message. 
    
    Args:
    - state: State
    - new_message:str
    - new_image: bytes 
    
    
    
    Returns:
    - Page
    
    '''
    headered_message= prepend_header(new_message)
    state.encoded_msg= new_message
    
    binary_message = message_to_binary(headered_message)
    state.message = binary_message
    state.msg_hist.append(state.encoded_msg)
    
    
    
    regular_image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')
    
    encoded_image= hide_bits(regular_image,state.message)
    state.encoded_img= encoded_image
    state.pup_coins +=1  
    
    return Page(state, ["Heres you image!",
                        Image(encoded_image,width=300,height=425),
                        "You earned a Pup coin!",
                        Button("Would you like to see the encoded message?",view_original_message),
                        Button("Home", index)
                        ])

@route
def view_original_message(state:State)->Page:
    '''
    Description: This is an option that displays the original message you sent
                to double check if you typed it correctly.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    original_message= state.encoded_msg
    encoded_image= state.encoded_img
    return Page(state,["Here's your original message with the encoded image:",
                       Image(encoded_image, width=300, height= 425),
                       original_message,
                       Button("Home", index)
                       
                       ])
                       
@route
def msg_history(state:State)->Page:
    '''
    Description : This function allows you to look back at
                    previously encoded messages.
    
    Args:
    - state: State
    
    
    
    Returns:
    - Page
    
    '''
    result= None
    if not state.msg_hist:
        
        result= Page(state, ["It seems that you haven't sent any messages!!",
                            Button("Back",index)
                            ])
        return result
    
    else:
        msg_list= state.msg_hist
        new_list=[]
        for message in msg_list:
            new_list.append(message)
            
            result= Page(state,["Here's your messages:",
                       NumberedList(new_list),
                       Button("Back",index)
                        ])
            
        return result
                        
    return result
                    
                       
    
          
      
#------ Decoder Helper Functions ----------

def even_or_odd_bit(num:int)->str:
    '''
    This function determines if a number is even or odd
    using the modulo operator.
    
    Args:
        - num (int)
       
    Returns
        - str
    '''
    if num % 2 == 1:
        number= '1'
    elif num % 2 == 0:
        number= '0'
    return number
    
assert_equal(even_or_odd_bit(3),'1')
assert_equal(even_or_odd_bit(5),'1')
assert_equal(even_or_odd_bit(6),'0')
assert_equal(even_or_odd_bit(12),'0')
        
        
def decode_single_char(intensity_values: list[int] )-> str:
    '''
    This function grabs a list of integers and converts them into a binary string
    based on if it is even or odd via the even_or_odd_bit function defined earlier.
    
    Args:
        - nums: (list[int])
        
    Returns:
        - str

    '''
    new_message = ''
    if len(intensity_values) != 8:
        return ''
    else:
        for number in intensity_values:
            char= even_or_odd_bit(number)
            new_message += char
        convert= int(new_message,2)
        new_char= chr(convert)
        return new_char
    
num_list= [22,22,23,22,23,22]
num_list1= [44,45,44,45,46,46,44,47]
num_list2= [33,33,32,34,33,33,32,33,34,33]
num_list3= [55,54,55,54,55,54,55,54]
num_list4= [46, 47, 46, 46, 47, 44, 46, 44]

assert_equal(decode_single_char(num_list),'')
assert_equal(decode_single_char(num_list1),'Q')
assert_equal(decode_single_char(num_list2),'')
assert_equal(decode_single_char(num_list3),'ª')
assert_equal(decode_single_char(num_list4), "H")



def decode_chars(intensity_values:list[int], quantity:int)->str:
    """
    Description: This function takes in a list of intensity values and the
    quantity of characters that you want to decode and converts them into 
    string characters for a message.
    
    Args:
    
    -intensity_values:list[int]
    -quantity: int

    Returns:
    
    -

    """
    
    new_message= ''
    if len(intensity_values) != 8 * quantity:
        return None
    else:          
        for num in range(0,quantity*8,8):
            decoded= decode_single_char(intensity_values[num:num+8])
            new_message += decoded
    return new_message

list_1=[22,22,22,23,24,24,24,24,
        24,25,25,25,25,25,26,26,
        26,27,27,27,27,26,26,26,
        ]

list_2=[44,45,44,45,47,44,43,47,
        44,45,45,45,45,45,46,46,
        ]

list_3=[22,22,23,23,22,23,22,23,
        24,25,25,25,25,25,26,26,
        26,27,27,27,27,26,26,26,
       ]

assert_equal(decode_chars(list_1,3),"\x10|x")
assert_equal(decode_chars(list_2,2),"[|")
assert_equal(decode_chars(list_3,3),"5|x")

def get_message_length(color_vals:list[int], header_count:int)->int:
    slice_cap = 8* header_count
    if len(color_vals) < slice_cap:
        return 0
    capped_values = color_vals[:slice_cap]
    message= decode_chars(capped_values, header_count)
    if message.isdigit():
        return int(message)
    return 0 

assert_equal(get_message_length([20, 254, 45, 95, 40, 90, 20, 40, 200, 254, 45,
                           95, 40, 95, 20, 45,220, 250, 45, 95, 48, 95, 24, 44], 2), 5)
    
assert_equal(get_message_length([20, 254, 45, 95, 40, 90, 20, 40, 200, 254, 45,
                           95, 40, 95, 20, 45,220, 250, 45, 95, 48, 95, 24, 44], 3), 54)

assert_equal(get_message_length([10, 120, 15, 5, 10, 10, 5, 40, 200, 254, 45,
                           95, 40, 90, 20, 45], 2), 21)

assert_equal(get_message_length([10, 122, 22, 22, 23, 10, 25, 40, 205, 254, 45,
                           95, 40, 90, 20, 45], 2), 0)

def get_encoded_message(color_intensities: list[int])->str:
    header= color_intensities[:24]
    message_length= get_message_length(header,3)
    message= decode_chars(color_intensities[24:message_length*8+24],message_length) 
    return message

assert_equal(get_encoded_message([254, 254, 255, 255, 254, 254, 254, 254, 
                           254, 254, 255, 255, 254, 254, 254, 254, 
                           254, 254, 255, 255, 254, 254, 255, 254, 
                           254, 255, 254, 254, 255, 254, 254, 254, 
                           254, 255, 255, 254, 255, 254, 254, 255, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           252]), "Hi" )


def get_color_values(image: PIL_Image, channel_num:int)->list[int]:
    """
    Description: Get color values function grabs values according to
                the channel number (Red, Green, or Blue). It is later
                evaluated in a loop column for column by loop in the x
                axis and then for each y value in the column.
                
    Args:
        - image: PIL_image
        - channel_num: int
    
    Returns:
        - list[int]
        - This is a list of color intensities in a
          specific channel (red, green, or blue).
    
    """
    width, length = image.size
    intensities = []
    if channel_num == 0:
        for x in range(width):
            for y in range(length):
                color_val = image.getpixel((x,y))
                red_value = color_val[0]
                intensities.append(red_value)
    
    elif channel_num == 1:
        for x in range(width):
            for y in range(length):
                color_val = image.getpixel((x,y))
                green_value = color_val[1]
                intensities.append(green_value)
         
    elif channel_num == 2:
       for x in range(width):
            for y in range(length):
                color_val = image.getpixel((x,y))
                blue_value = color_val[2]
                intensities.append(blue_value)
    return intensities         

#------ Encoder Helper Functions ----------

def get_message(max_chars:int)->str:
    """
    Description: Function takes in an int that caps off how many characters that a message
    can have. The message is inputted by the user. Should the user exceed the character cap,
    the program asks for the user to type in another message that meets the length parameter.
    
    Args:
        - max_chars: int
    
    Returns:
        - message: str
    
    """
    message= input("What message do you want to send?")
    while len(message)>max_chars:
        print(message)
        message=input()
    
    return message

#assert_equal(get_message(3),"bea")
#assert_equal(get_message(5),"beans")
#assert_equal(get_message(9),"Spikedawg")    
#assert_equal(get_message(14),"Dogs_are_cool")

    
    
def message_to_binary(message:str)->str:
    """
    Description: Function takes the message that you wish to encode and 
    converts it into a binary string of 0's and 1's.
    
    Args:
        -message :str
    Returns:
        -binary_str :str
        
    """
    
    binary_str = ''
    for character in message:
        convert_char = ord(character)
        binary_line= format(convert_char, '08b')
        binary_str += binary_line
    return binary_str

assert_equal(message_to_binary("Hi"), "0100100001101001")
assert_equal(message_to_binary("058"),"001100000011010100111000")
assert_equal(message_to_binary("beans"),"0110001001100101011000010110111001110011")
assert_equal(message_to_binary("spikedawg"),"011100110111000001101001011010110110010101100100011000010111011101100111")
             
        
def prepend_header(message:str)->str:
    """
    Description: This function takes in a regular string and measures it's length.
    It determines how many digit amount of the length of the string and converts
    it into a string. Afterwards it adds the message string to the original length
    string to return the number of characters before the message.
    
    Args:
        - message : str
        
    Returns:
        - message with perpended character count: str


    """
    msg_length = len(message)
    if msg_length == 0:
        return '000'
    
    elif msg_length in range(1,10):
        header_nums = '00'
        return header_nums + str(msg_length) + message
    
    elif msg_length in range(10,100):
        header_nums = '0'
        return header_nums + str(msg_length) + message
    
    elif msg_length in range(100,1000):
        header_nums = ''
        return header_nums + str(msg_length) + message
    

    
                
assert_equal(prepend_header("Beans"),"005Beans")             
assert_equal(prepend_header("Hi"),"002Hi")
assert_equal(prepend_header("Spikedawgs"),"010Spikedawgs")
assert_equal(prepend_header("""This Message is Over Hundred Characters,
                              I Must Test This Because If Not, Nazim Will Yell
                               At Me. I Get Its Neccessary But This Is Just Silly."""),
             
                             """202This Message is Over Hundred Characters,
                              I Must Test This Because If Not, Nazim Will Yell
                               At Me. I Get Its Neccessary But This Is Just Silly."""),
             
    
def new_color_value(base_10_val:int, bit:str)->int:
    """
    Description: Function takes in a base_10 color intensity value
    along with a specific 'bit' which can either be '0', or '1'. It determines which
    one the bit is and then changes the color value by an increment of 1, depending on
    if the intensity value is even or odd. 

    Args:
        - base_10_val : int
        - bit : str
        
    Returns:
        - updated color value :int
        
    """
    if '1' in bit:
        if base_10_val % 2 == 0:
            base_10_val += 1
            return base_10_val
        else:
            return base_10_val
        
    elif '0' in bit:
        if base_10_val % 2 == 1:
            base_10_val -=1
            return base_10_val
        else:
            return base_10_val
        
assert_equal(new_color_value(77,'1'),77)
assert_equal(new_color_value(36,'1'),37)
assert_equal(new_color_value(54,'0'),54)
assert_equal(new_color_value(23,'0'),22)

def hide_bits(image: PIL_Image, binary_str:str)->PIL_Image:
     width , length = image.size
     binary_index= 0
     for x in range(width):
            for y in range(length):
                if binary_index< len(binary_str):
                    red_num,green_num,blue_num = image.getpixel((x,y))                  
                    new_green_val = new_color_value(green_num, binary_str[binary_index])
                    image.putpixel((x,y),(red_num ,new_green_val,blue_num))
                    binary_index+=1
     return image              


assert_equal(
 index(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=["Welcome to Spike's Silly Doggo Website!",
              'Send Puppers with messages to your buddies!!',
              Image(url='Spike_2.png', width=300, height=425),
              Button(text='Import Pupper', url='/import_pupper'),
              Button(text='Export Pupper', url='/export_pupper'),
              Button(text='How-to', url='/how_to'),
              Button(text='Pup Coins', url='/pup_coins'),
              Button(text='Meet Spike', url='/our_creator'),
              Button(text='Message History', url='/msg_history')]))
 
assert_equal(
 how_to(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=['How to Guides:',
              Button(text='How to send encoded images?', url='/how_to_send'),
              Button(text='How to decode images?', url='/how_to_view'),
              Button(text='Home', url='/')]))

assert_equal(
 how_to_send(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=["If 'Send Pupper' selected:",
              'Step 1: You will be prompted to upload a picture of a pupper.',
              'Step 2: Once photo is uploaded, type message you want to send.',
              'Step 3: Download the new image of pupper with message.',
              'Step 4: Success! You earned a Pup coin!!',
              Button(text='Back', url='/how_to')]))


assert_equal(
 how_to_view(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=["If 'Import Pupper' selected:",
              'Step 1: You will be prompted to upload this image',
              "Note: You can view the image by clicking 'Display'",
              "Step 2: You can decode you message by clicking 'decode'",
              'Step 3: View your silly decoded message!',
              'Step 4: Success! You earned a Pup coin!!',
              Button(text='Back', url='/how_to')]))

assert_equal(
 pup_coins(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=['You have 0 pup coins', 'Send or Receive some Puppers for pup coins!! :)', Button(text='Home', url='/')]))

assert_equal(
 our_creator(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
     content=[" Meet Spike, the creator's beloved Rottweiler,\n"
              '                        who is the main face of thie website and inspiration\n'
              '                        for the Silly Doggo Website.',
              Image(url='me&spike.png', width=200, height=325),
              'Would you like to give spike a pup coin?',
              Button(text='Yes', url='/give_pup_coin'),
              Button(text='No', url='/'),
              Button(text='Home', url='/')]))

assert_equal(
 give_pup_coin(State(message=None, pup_coins=0, image=None, decoded_msg=None, encoded_msg=None, msg_hist=[], error_msg=None, spikes_coins=0, encoded_img=None)),
 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg='Whoops, you dont have any pup coins :(',
                 spikes_coins=0,
                 encoded_img=None),
     content=['Whoops, you dont have any pup coins :(',
              Image(url='pensivespike.png', width=300, height=425),
              'Send or receive messages to earn pup coins!!',
              Button(text='Home', url='/')]))


assert_equal(
 give_pup_coin(State(message=None,
                     pup_coins=1, 
                     image=None, 
                     decoded_msg=None, 
                     encoded_msg=None,
                     msg_hist=[], error_msg=None,
                     spikes_coins=0, 
                     encoded_img=None)),
                 Page(state=State(message=None,
                 pup_coins=0,
                 image=None,
                 decoded_msg=None,
                 encoded_msg=None,
                 msg_hist=[],
                 error_msg=None,
                 spikes_coins=1,
                 encoded_img=None),
     content=['Yay!! Spike is happy!!',
              Image(url='happyspike.png', width=300, height=425),
              'He thanks you for your kindness.',
              Button(text='Home', url='/')]))


assert_equal(
    view_original_message(State(
    message='0011000000110000001101010100010101110100011010000110000101101110',
    pup_coins=1,
    image=None,
    decoded_msg=None,
    encoded_msg='Ethan',
    msg_hist=['Ethan'],
    error_msg=None,
    spikes_coins=0,
    encoded_img=None)),
    Page(state=State(message='0011000000110000001101010100010101110100011010000110000101101110',
                 pup_coins=1,
                 image=None,
                 decoded_msg=None,
                 encoded_msg='Ethan',
                 msg_hist=['Ethan'],
                 error_msg=None,
                 spikes_coins=0,
                 encoded_img=None),
              content=["Here's your original message with the encoded image:",
              Image(url=None, width=300, height=425),
              'Ethan',
              Button(text='Home', url='/')]))

start_server(State(None,0,None,None,None,[],None,0,None))
    
