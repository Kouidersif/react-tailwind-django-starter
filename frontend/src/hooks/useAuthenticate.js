import axiosInstance from "@/api/api"




const useAuthenticate = () => {
    const loginUser = async (data) => {
        try {
            const response = await axiosInstance.post("/login/", data)
            console.log("response: ", response)
        } catch (error) {
            console.log("error: ", error)
        } finally {
            console.log("done: ")
        }
    }

    const registerUser = async (data) => {
        try {
            const response = await axiosInstance.post("/register/", data)
            console.log("response: ", response)
        } catch (error) {
            console.log("error: ", error)
        }
    }

    const validateCode = async (data) => {
        try {
            const response = await axiosInstance.post("/validate-code/", data)
            console.log("response: ", response)
        } catch (error) {
            console.log("error: ", error)
        }
    }

    const resendCode = async (data) => {
        try {
            const response = await axiosInstance.post("/resend-code/", data)
            console.log("response: ", response)
        } catch (error) {
            console.log("error: ", error)
        }
    }

    return {
        loginUser,
        registerUser,
        validateCode,
        resendCode
    }
}

export default useAuthenticate