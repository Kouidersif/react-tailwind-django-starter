import useAuthenticate from "@/hooks/useAuthenticate";
import { useAuth0 } from "@auth0/auth0-react";
import { Button, Card, Label, TextInput, Checkbox, Select } from "flowbite-react";
import { useState } from "react";
import { FaGoogle, FaLinkedin } from "react-icons/fa";

const Register = () => {
    const { loginWithRedirect } = useAuth0();
    const { registerUser } = useAuthenticate();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        password2: "",
        gender: "",

    })

    const handleAuthLogin = (connection) => {
        loginWithRedirect({
            authorizationParams: {
                connection,
            }
        });
    }

    const handleRegister = async (e) => {
        e.preventDefault();
        // eslint-disable-next-line no-unused-vars
        const response = await registerUser(formData)
    }
    return (
        <Card className="w-full">
            <div className="space-y-6">
                <h3 className="text-xl font-medium text-gray-900 dark:text-white">
                    Create an account
                </h3>
                <form onSubmit={handleRegister} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-3">
                        <div>
                            <div className="mb-2 block">
                                <Label htmlFor="firstName" value="First Name *" />
                            </div>
                            <TextInput
                                id="firstName"
                                placeholder="John"
                                required
                                type="text"
                                value={formData.first_name}
                                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                            />
                        </div>
                        <div>
                            <div className="mb-2 block">
                                <Label htmlFor="lastName" value="Last Name *" />
                            </div>
                            <TextInput
                                id="lastName"
                                placeholder="Doe"
                                required
                                value={formData.last_name}
                                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                                type="text"
                            />
                        </div>
                    </div>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="email" value="Email *" />
                        </div>
                        <TextInput
                            id="email"
                            placeholder="name@company.com"
                            required
                            type="email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        />
                    </div>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="gender" value="Gender" />
                        </div>
                        <Select
                            id="gender"
                            required
                            value={formData.gender}
                            onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                        >
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Prefer not to say">Prefer not to say</option>
                        </Select>
                        
                    </div>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="password" value="Password *" />
                        </div>
                        <TextInput
                            id="password"
                            required
                            placeholder="••••••••"
                            type="password"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        />
                    </div>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="password2" value="Confirm Password *" />
                        </div>
                        <TextInput
                            id="password2"
                            required
                            placeholder="••••••••"
                            type="password"
                            value={formData.password2}
                            onChange={(e) => setFormData({ ...formData, password2: e.target.value })}
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Checkbox id="remember" />
                            <Label htmlFor="remember">Remember me</Label>
                        </div>
                        <a href="#" className="text-sm text-cyan-700 hover:underline dark:text-cyan-500">
                            Forgot password?
                        </a>
                    </div>
                    <Button type="submit" className="w-full">
                        Register
                    </Button>
                </form>
                <div className="flex items-center justify-center">
                    <span className="text-sm text-gray-500">or continue with</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                    <Button color="gray" className="w-full" onClick={() => handleAuthLogin("google-oauth2")}>
                        <FaGoogle className="h-4 w-4 mr-2" fill="red" />
                        <p>
                            Login with Google
                        </p>
                    </Button>
                    <Button color="gray" className="w-full" onClick={() => handleAuthLogin("linkedin")}>
                        <FaLinkedin className="h-4 w-4 mr-2" fill="blue" />
                        <p>
                            Login with LinkedIn
                        </p>
                    </Button>
                </div>
                <p className="text-sm text-gray-500 text-center">
                    Don{"'"}t have an account?{" "}
                    <a href="#" className="text-cyan-700 hover:underline dark:text-cyan-500">
                        Sign up
                    </a>
                </p>
            </div>
        </Card>
    );
};

export default Register;