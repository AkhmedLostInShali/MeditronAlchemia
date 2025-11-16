import "./MainPage.css"

const MainPage = () => {
    return (
        <div className="main-page">
            <header>
                <div className="left-side">
                    <button>file</button>
                    <button>options</button>
                </div>

                <div className="right-side">
                    <img src="icons/profile.png" alt="" />
                    <div className="username">Сальников А.</div>
                </div>
            </header>

            <div className="patients-side">
                <div className="search">
                    <input type="text" placeholder="Найти пациента" />
                    <button>ID <span className="arrow">↓</span></button>
                </div>

                <div className="patients-list">
                    <div className="active">#133325</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                    <div>#553452</div>
                    <div>#937191</div>
                    <div>#294720</div>
                </div>

                <div className="add-patient">
                    Добавить пациента
                </div>
            </div>

            <div className="modal-background">
                <div className="modal">
                    <div className="modal-form">
                        <h3>Создание пациента</h3>
                        <p>Заполните данные</p>
                        <div className="input_block">
                            <label htmlFor="">Псевдоним</label>
                            <input type="text" className="nickname" value="Ванильный тиранозавр" disabled />
                        </div>
                        <div className="input_block">
                            <label htmlFor="">Возраст</label>
                            <input type="number" />
                        </div>
                        <div className="input_block">
                            <label htmlFor="">Раса</label>
                            <select name="" id="">
                                <option value="">Белый</option>
                                <option value="">Темнокожий</option>
                                <option value="">Азиат</option>
                            </select>
                        </div>

                        <div className="input_block">
                            <label htmlFor="">Молекулярный подтип</label>
                            <select name="" id="">
                                <option value="">HR+HER2</option>
                                <option value="">HR+HER2+</option>
                                <option value="">HR-HER2+</option>
                            </select>
                        </div>

                        <div className="input_block">
                            <label htmlFor="">Менопауза</label>
                            <select name="" id="">
                                <option value="">Пременопауза</option>
                                <option value="">Постменопауза</option>
                                <option value="">Переменопауза</option>
                            </select>
                        </div>
                    </div>
                    <div className="buttons">
                        <button className="cancer">Отмена</button>
                        <button className="apply">Создать</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MainPage