import "./Auth.css"

const Auth = () => {
    return <div className="auth-page">
        <div className="auth-form">
            <h1>Вход</h1>
            <input type="text" placeholder="Введите логин" />
            <input type="password" placeholder="Введите пароль" />
            <input text="Войти" type="submit" />
            
        </div>
    </div>
}

export default Auth;