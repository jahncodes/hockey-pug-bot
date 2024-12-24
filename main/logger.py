from colorama import Back, Fore, Style
import time

def getPrefix():
    """
    getPrefix styles and formats current time for console messages.
    
    returns: (string) with proper formatting and styling.
    """
    return (Fore.GREEN + time.strftime("%H:%M:%S EST", time.localtime()) + Fore.WHITE + Style.BRIGHT)
    

def infoLog(messageOne, messageTwo):
    """
    infoLog sends an information messa ge to console with proper formatting with time and color styling for readibility. 
    """
    print(getPrefix() + Fore.WHITE + ' ' + messageOne + Fore.BLUE + ' ' + messageTwo)
    
def successLog(message):
    """
    successLog sends an information message to console with proper formatting with time and color styling for readibility. 
    """
    print(getPrefix() + Fore.GREEN + ' ' + message)
       
def warningLog(message):
    """
    warningLog sends warning message to console with proper formatting with time and color styling for readibility. 
    """
    print(getPrefix() + Fore.YELLOW + ' ' + message)
    
    
def errorLog(message):
    """
    errorLog sends error message to console with proper formatting with time and color styling for readibility. 
    """
    print(getPrefix() + Fore.RED + ' ' + message)
