import { useAuth0 } from "@auth0/auth0-react";
import { Card, Spinner } from "flowbite-react";



const Auth0Callback = () => {
    const { user } = useAuth0();

    
    return (
        <Card className="w-full">
            <div className="space-y-6">
                <div className="text-center">
                    <h3 className="text-xl font-medium text-gray-900 dark:text-white">
                        Authenticating
                    </h3>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                        Please wait while we verify your credentials
                    </p>
                </div>

                <div className="flex justify-center py-8">
                    <Spinner size="xl" />
                </div>

                <p className="text-sm text-gray-500 text-center">
                    You will be redirected automatically
                </p>
            </div>
        </Card>
    );
};

export default Auth0Callback;