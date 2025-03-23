import useAuthenticate from "@/hooks/useAuthenticate";
import { Button, Card, Label, TextInput } from "flowbite-react";
import { useState } from "react";
import { useParams } from "react-router-dom";

const VerifyCode = () => {
    const { validateCode, resendCode } = useAuthenticate();
    const { email } = useParams();
    const [formData, setFormData] = useState({
        code: "",
        flag: "email"
    })
    const handleSubmit = async (e) => {
        e.preventDefault();
        // eslint-disable-next-line no-unused-vars
        const response = await validateCode(formData)
    }

    const handleResend = async () => {
        // eslint-disable-next-line no-unused-vars
        const response = await resendCode({ email, flag: "email" })
    }
    return (
        <Card className="w-full">
            <div className="space-y-6">
                <div className="text-center">
                    <h3 className="text-xl font-medium text-gray-900 dark:text-white">
                        Verify your email
                    </h3>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                        We{"'"}ve sent a code to your email
                    </p>
                </div>

                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="code" value="Enter verification code" />
                        </div>
                        <TextInput
                            id="code"
                            type="text"
                            maxLength={6}
                            className="text-center tracking-[1em]"
                            placeholder="······"
                            required
                            onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                            value={formData.code}
                        />
                    </div>

                    <Button type="submit" className="w-full">
                        Verify Email
                    </Button>
                </form>

                <div className="text-center">
                    <p className="text-sm flex justify-center items-center gap-2 text-gray-500">
                        Didn{"'"}t receive the code?{" "}
                        <Button color="gray" onClick={handleResend} size="xs" className="px-0" pill>
                            Resend
                        </Button>
                    </p>
                </div>

            </div>
        </Card>
    );
};

export default VerifyCode;